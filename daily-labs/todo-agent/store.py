"""웹과 MCP가 같은 DB를 읽는다. 처음 실행할 때만 기존 Todo JSON을 가져온다."""
import json
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

BASE = Path(__file__).resolve().parent

def db_path():
    return Path(os.getenv("TODO_DB") or BASE / "todo.sqlite3").resolve()

@contextmanager
def database():
    db = sqlite3.connect(db_path())
    db.row_factory = sqlite3.Row
    try:
        with db:
            yield db
    finally:
        db.close()

def initialize():
    with database() as db:
        db.execute("BEGIN IMMEDIATE")
        db.execute("CREATE TABLE IF NOT EXISTS todos(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, done INTEGER NOT NULL, version INTEGER NOT NULL)")
        db.execute("CREATE TABLE IF NOT EXISTS proposals(token TEXT PRIMARY KEY, item INTEGER, done INTEGER, version INTEGER, status TEXT)")
        if db.execute("PRAGMA user_version").fetchone()[0] == 0 and not db.execute("SELECT 1 FROM todos LIMIT 1").fetchone():
            rows = json.loads((BASE / "tasks.json").read_text(encoding="utf-8"))
            db.executemany("INSERT INTO todos VALUES(?,?,?,0)", [(r["id"], r["title"], r["done"]) for r in rows])

        db.execute("PRAGMA user_version=1")

def add_item(title):
    with database() as db:
        return db.execute("INSERT INTO todos(title,done,version) VALUES(?,0,0)", (title,)).lastrowid

def edit_item(item, version, title, done):
    with database() as db:
        changed = db.execute("UPDATE todos SET title=?, done=?, version=version+1 WHERE id=? AND version=?",
                             (title, done, item, version))
        return bool(changed.rowcount)

def remove_item(item, version):
    with database() as db:
        return bool(db.execute("DELETE FROM todos WHERE id=? AND version=?", (item,version)).rowcount)

def list_items():
    with database() as db:
        return [{**dict(row), "done": bool(row["done"])} for row in db.execute("SELECT * FROM todos ORDER BY id")]

def propose(token, item, done, version):
    with database() as db:
        db.execute("INSERT INTO proposals VALUES(?,?,?,?,'pending')", (token,item,done,version))

def decide(token, approve):
    with database() as db:
        db.execute("BEGIN IMMEDIATE")
        row = db.execute("SELECT * FROM proposals WHERE token=?", (token,)).fetchone()
        if row is None:
            raise KeyError(token)
        if row["status"] != "pending":
            return row["status"]
        status = "rejected"
        if approve:
            changed = db.execute("UPDATE todos SET done=?,version=version+1 WHERE id=? AND version=?",
                                 (row["done"],row["item"],row["version"]))
            status = "applied" if changed.rowcount else "conflict"
        db.execute("UPDATE proposals SET status=? WHERE token=?", (status,token))
        return status
