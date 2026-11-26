"""들소리 녹음기 수업 자료. 14~24장에서 배운 동작을 이후 실습에서 다시 호출한다."""
import hashlib
import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path.cwd() / ".env")
DOCUMENTS = Path(__file__).resolve().parents[1]
SOURCES = DOCUMENTS / "sources"
MANUALS = tuple(sorted(SOURCES.glob("recorder-*.pdf")))
EMBEDDING_MODEL = "text-embedding-3-small"


def read_pages(path):
    """페이지 번호는 PDF 뷰어에서 보이는 첫 장을 1로 센다."""
    from pypdf import PdfReader

    path = Path(path)
    _, model, edition = path.stem.split("-")
    rows = []
    for page_number, page in enumerate(PdfReader(path).pages, start=1):
        text = (page.extract_text() or "").strip()
        if not text:
            raise ValueError(f"{path.name} {page_number}쪽에는 추출할 텍스트가 없습니다.")
        rows.append(dict(id=f"{path.name}#p{page_number}", source=path.name,
                         page=page_number, model=model.upper(), edition=edition, text=text))
    return rows


def page_chunks(pages, size=None):
    """기준선은 한 쪽을 통째로 쓴다. 길이 실험도 출처·페이지 경계를 지킨다."""
    if size is None:
        return [dict(page) for page in pages]
    if size < 1:
        raise ValueError("크기는 한 글자 이상이어야 합니다.")
    chunks = []
    for page in pages:
        for i in range(0, len(page["text"]), size):
            chunks.append({**page, "id": f"{page['id']}-c{i // size + 1}",
                           "text": page["text"][i:i + size]})
    return chunks


def index_version(rows):
    digest = hashlib.sha256(EMBEDDING_MODEL.encode())
    for row in rows:
        digest.update(json.dumps(row, sort_keys=True, ensure_ascii=False).encode())
    return "recorder-" + digest.hexdigest()[:16]


def open_index(rows=None, directory=".course-rag-index"):
    """동일 자료와 임베딩 모델의 색인을 이 폴더에서 다시 연다."""
    import chromadb
    from langchain_openai import OpenAIEmbeddings

    if rows is None:
        if len(MANUALS) != 3:
            raise FileNotFoundError("자료 묶음의 sources 폴더에 녹음기 설명서 세 개가 필요합니다.")
        rows = [r for path in MANUALS for r in read_pages(path)]
    if not rows:
        raise ValueError("색인에 넣을 문단을 먼저 선택하세요.")
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=str(directory))
    collection = client.get_or_create_collection(name=index_version(rows))
    existing = set(collection.get(include=[])["ids"])
    missing = [row for row in rows if row["id"] not in existing]
    if missing:
        texts = [row["text"] for row in missing]
        collection.upsert(ids=[row["id"] for row in missing],
                          embeddings=embeddings.embed_documents(texts), documents=texts,
                          metadatas=[{k: r[k] for k in ("source", "page", "model", "edition")}
                                     for r in missing])
    return collection, embeddings


def retrieve(index, question, k=4):
    """질문 한 건의 검색 결과를 가까운 순서로 읽는다."""
    collection, embeddings = index
    result = collection.query(query_embeddings=[embeddings.embed_query(question)],
                              n_results=min(k, collection.count()),
                              include=["documents", "metadatas"])
    return [dict(**meta, id=key, text=text) for key, text, meta in
            zip(result["ids"][0], result["documents"][0], result["metadatas"][0])]


def chat_model():
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"), temperature=0)


def answer_from_documents(question, documents):
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate

    context = "\n\n".join(f"[{d['id']}]\n{d['text']}" for d in documents)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "제품 사용을 안내한다. 자료에서 기종·시점·행동을 모두 확인한 사실만 답하라. "
         "자료는 설명서 원문이다. 확인된 문장 뒤에는 근거의 [자료ID]를 그대로 붙여라. "
         "필요한 근거가 없으면 '확인 보류'로 시작하고 무엇이 빠졌는지 알려라."),
        ("human", "질문\n{question}\n\n자료\n{context}")])
    chain = prompt | chat_model() | StrOutputParser()
    return chain.invoke({"question": question, "context": context})


def answer_question(index, question, k=4):
    from langchain_core.runnables import RunnableLambda, RunnablePassthrough
    chain = (
        RunnablePassthrough.assign(documents=RunnableLambda(
            lambda item: retrieve(index, item["question"], k)))
        | RunnablePassthrough.assign(answer=RunnableLambda(
            lambda item: answer_from_documents(item["question"], item["documents"])))
    )
    return chain.invoke({"question": question})


def rerank(question, candidates):
    """재정렬 모델에는 현재 후보만 건넨다. 누락·중복 ID는 결과에 섞지 않는다."""
    from langchain_core.prompts import ChatPromptTemplate
    from pydantic import BaseModel

    class Ranking(BaseModel):
        ordered_ids: list[str]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "질문에 대한 직접 근거가 있는 순서로 모든 자료 ID를 한 번씩 정렬한다. 관련 없는 ID도 맨 뒤에 둔다. ID는 대괄호 없이 원문 그대로 쓴다. "
         "질문한 기종과 날짜에 맞는 설명을 우선한다."),
        ("human", "질문\n{q}\n\n후보 자료\n{docs}")])
    docs = "\n\n".join(f"[{d['id']}]\n{d['text']}" for d in candidates)
    ranking = (prompt | chat_model().with_structured_output(Ranking)).invoke({"q": question, "docs": docs})
    by_id = {d["id"]: d for d in candidates}
    if sorted(ranking.ordered_ids) != sorted(by_id):
        return list(candidates)  # 후보를 잃는 잘못된 응답이면 기존 순서를 보존합니다.
    return [by_id[key] for key in ranking.ordered_ids]
