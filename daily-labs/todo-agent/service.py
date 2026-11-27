from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from agents import handle
from store import add_item, decide, edit_item, initialize, list_items, remove_item

@asynccontextmanager
async def lifespan(app):
    initialize()
    yield

app = FastAPI(lifespan=lifespan)

class Request(BaseModel):
    question: str = Field(min_length=1, max_length=1000)

class Decision(BaseModel):
    approve: bool

@app.get("/")
def home():
    return FileResponse(Path(__file__).with_name("index.html"))

@app.get("/api/todos")
def todos():
    return list_items()

class NewTodo(BaseModel):
    title: str = Field(min_length=1, max_length=200, pattern=r"\S")

class TodoEdit(NewTodo):
    done: bool
    version: int = Field(ge=0)

@app.post("/api/todos", status_code=201)
def create_item(body: NewTodo):
    return {"id": add_item(body.title.strip())}

@app.put("/api/todos/{item}")
def replace_item(item: int, body: TodoEdit):
    if not edit_item(item, body.version, body.title.strip(), body.done):
        raise HTTPException(409, "목록을 다시 조회하세요.")
    return {"status": "applied"}

@app.delete("/api/todos/{item}")
def delete_item(item: int, version: int):
    if not remove_item(item, version):
        raise HTTPException(409, "목록을 다시 조회하세요.")
    return {"status": "deleted"}

@app.post("/api/agent")
async def ask(body: Request):
    return await handle(body.question)

@app.post("/api/proposals/{token}")
def confirm(token: str, body: Decision):
    try:
        status = decide(token, body.approve)
    except KeyError:
        raise HTTPException(404, "제안을 찾을 수 없습니다.")
    if status == "conflict":
        raise HTTPException(409,"그동안 할 일이 바뀌었습니다. 다시 조회하세요.")
    return {"status":status}
