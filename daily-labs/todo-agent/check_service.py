"""완성한 API를 임시 DB로 점검한다. 현재 작업 중인 할 일은 그대로 보존된다."""
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from fastapi.testclient import TestClient
from service import app
from store import propose


def check():
    with TemporaryDirectory() as folder, patch.dict(os.environ, {"TODO_DB": str(Path(folder) / "check.db")}):
        with TestClient(app) as client:
            new = client.post("/api/todos", json={"title": "인수 시험"})
            assert new.status_code == 201
            item = new.json()["id"]
            for token in ["withdraw", "stale", "accept", "later"]:
                propose(token, item, True, 0)

            def decision(token, approve):
                return client.post("/api/proposals/" + token, json={"approve": approve})

            assert decision("withdraw", False).json()["status"] == "rejected"
            assert decision("accept", True).json()["status"] == "applied"
            assert decision("accept", True).json()["status"] == "applied"
            assert decision("stale", True).status_code == 409
            saved = next(row for row in client.get("/api/todos").json() if row["id"] == item)
            assert saved["done"] and saved["version"] == 1
            propose("before-edit", item, False, 1)
            assert client.put(f"/api/todos/{item}", json={**saved, "title": "직접 편집"}).is_success
            assert decision("before-edit", True).status_code == 409
            assert client.delete(f"/api/todos/{item}?version=2").is_success
            assert all(row["id"] != item for row in client.get("/api/todos").json())
            print("승인·거절·중복 승인·버전 충돌과 웹 편집 확인")


if __name__ == "__main__":
    check()
