from mcp.server.fastmcp import FastMCP
from store import list_items

server = FastMCP("todo-reader")

@server.tool()
def list_todos() -> list[dict]:
    """할 일의 실제 ID, 제목, 완료 여부와 버전을 조회한다."""
    return list_items()

if __name__ == "__main__":
    server.run(transport="stdio")
