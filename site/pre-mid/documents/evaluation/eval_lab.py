"""녹음기 수업의 CSV와 이전 장의 챗봇을 평가 화면에 연결하는 준비 코드."""
import csv
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid5

DOCS = Path(__file__).resolve().parents[1]
for folder in ("rag", "graph"):
    if str(DOCS / folder) not in sys.path:
        sys.path.insert(0, str(DOCS / folder))

# 수강자가 챗봇 화면에서 선택한 기종·판본. 정답 문서와 쪽수는 입력에 넣지 않는다.
DEVICE = {
    "D01": ("A", "1.1"), "D02": ("B", "1.0"), "D03": ("A", "1.0"),
    "D04": ("A", "1.1"), "D05": ("B", "1.0"), "H01": ("B", "1.0"),
    "H02": ("A", "1.1"), "H03": ("B", "1.0"), "H04": ("A", "1.1"),
}


def read_rows(part, split):
    with (DOCS / part / f"recorder-{split}.csv").open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def examples(split):
    references = {row["id"]: row for row in read_rows("answers", split)}
    result = []
    for row in read_rows("questions", split):
        key = row["id"]
        device, edition = DEVICE[key]
        ref = references[key]
        result.append({
            "inputs": dict(id=key, question=row["question"], model=device, edition=edition),
            "outputs": dict(action=ref["expected_action"], source=ref["source"],
                            page=int(ref["page"]) if ref["page"] else None,
                            reference_answer=ref["reference_answer"]),
        })
    return result


def dataset_for(client, split, rows):
    # 행의 내용이 달라지면 새 평가 세트를 만들어 예전 실험을 다시 열 수 있게 한다.
    payload = json.dumps(rows, sort_keys=True, ensure_ascii=False).encode()
    version = hashlib.sha256(payload).hexdigest()[:12]
    name = f"recorder-{split}-{version}"
    ds = client.read_dataset(dataset_name=name) if client.has_dataset(dataset_name=name) else client.create_dataset(name)
    known = {e.id for e in client.list_examples(dataset_id=ds.id)}
    missing = []
    for row in rows:
        example_id = uuid5(ds.id, row["inputs"]["id"])
        if example_id not in known:
            missing.append({"id": example_id, **row})
    if missing:
        client.create_examples(dataset_id=ds.id, examples=missing)
    return ds


def lcel_result(index, item, k):
    from rag_lab import answer_question
    raw = answer_question(index, item["question"], k=k)
    answer = raw["answer"]
    # 앞 장 체인이 실제로 답에 적은 인용과 검색기에 들어왔던 후보를 각각 보존한다.
    citations = re.findall(r"\[(recorder-[ab]-[0-9.]+\.pdf#p\d+)\]", answer)
    return dict(answer=answer, action="abstain" if answer.strip().startswith("확인 보류") else "answer",
                candidates=[p["id"] for p in raw["documents"]], citations=citations,
                path=["retrieve", "answer"])


def graph_result(graph, item):
    from recorder_graph import ask
    raw = ask(graph, item["question"], item["model"], item["edition"])
    return dict(answer=raw["answer"], action=raw["status"],
                candidates=[p["id"] for p in raw["documents"]],
                citations=[p["id"] for p in raw["citations"]], path=raw["path"],
                searches=[{"query": s["query"], "candidates": [p["id"] for p in s["documents"]]}
                          for s in raw["searches"]])


def gold_page(ref):
    if ref["action"] == "answer":
        return f"{ref['source']}#p{ref['page']}"
    return None


def assessment(outputs, reference_outputs):
    """문서 ID로 판정할 수 있는 항목만 계산한다. 답변 문장은 사람이 대조한다."""
    ref = reference_outputs
    gold = gold_page(ref)
    scores = [{"key": "action_match", "score": int(outputs["action"] == ref["action"])}]
    if gold:
        candidates = outputs["candidates"]
        rank = candidates.index(gold) + 1 if gold in candidates else None
        scores.extend([
            {"key": "retrieval_rr", "score": 1 / rank if rank else 0},
            {"key": "citation_has_gold", "score": int(gold in outputs["citations"])},
        ])
    return {"results": scores}


def make_targets(index, candidate_k):
    from recorder_graph import make_graph
    baseline = make_graph(index, k=4)
    candidate = make_graph(index, k=candidate_k)
    return {
        "lcel-k4": lambda inputs: lcel_result(index, inputs, 4),
        "graph-k4": lambda inputs: graph_result(baseline, inputs),
        f"graph-k{candidate_k}": lambda inputs: graph_result(candidate, inputs),
    }


def experiment_settings(index, k):
    # 코드와 프롬프트가 들어 있는 두 파일의 내용도 함께 식별한다.
    hashes = {}
    for path in (DOCS / "rag/rag_lab.py", DOCS / "graph/recorder_graph.py", Path(__file__)):
        hashes[path.stem] = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
    return dict(model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"), index_version=index[0].name,
                code_and_prompt=hashes, k=k)


def compare(client, split, rows, targets, index):
    ds = dataset_for(client, split, rows)
    # 같은 시점에 고정한 질문 리스트를 모든 실험이 공유한다.
    version = client.read_dataset_version(dataset_id=ds.id, as_of=datetime.now(timezone.utc)).as_of
    fixed = list(client.list_examples(dataset_id=ds.id, as_of=version))
    expected_ids = {row["inputs"]["id"] for row in rows}
    if {e.inputs["id"] for e in fixed} != expected_ids or len(fixed) != len(rows):
        raise ValueError("원격 세트의 질문 목록과 수업 CSV가 다릅니다. 질문 ID와 행 수를 확인하세요.")
    report = {}
    for label, target in targets.items():
        k = int(label.rpartition("k")[2])
        settings = experiment_settings(index, k)
        experiment = client.evaluate(target, data=fixed, evaluators=[assessment], max_concurrency=1,
                                     experiment_prefix=f"{split}-{label}", metadata={**settings, "dataset_as_of": str(version)})
        project = client.read_project(project_name=experiment.experiment_name)
        runs = []
        for result in experiment:
            run = result["run"]
            runs.append(dict(id=result["example"].inputs["id"], run_id=str(run.id), output=run.outputs,
                             error=run.error, scores=[r.model_dump(include={"key", "score"})
                                                      if hasattr(r, "model_dump") else r.dict(include={"key", "score"})
                                                      for r in result["evaluation_results"]["results"]]))
        report[label] = dict(experiment=experiment.experiment_name, experiment_id=str(project.id),
                             dataset=ds.name, dataset_id=str(ds.id), dataset_as_of=str(version),
                             settings=settings, rows=runs)
    return report
