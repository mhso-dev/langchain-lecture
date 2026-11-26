FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY agents.py service.py store.py todo_mcp.py index.html tasks.json ./
COPY skills/ ./skills/
ENV TODO_DB=/data/todo.sqlite3
RUN mkdir /data
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]
