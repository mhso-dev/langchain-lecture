import asyncio
import sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from store import db_path, initialize

async def check():
    initialize()
    params = StdioServerParameters(
        command=sys.executable, args=[str(Path(__file__).with_name("todo_mcp.py"))],
        env={"TODO_DB": str(db_path())},
    )
    async with stdio_client(params) as (reader,writer):
        async with ClientSession(reader,writer) as session:
            await session.initialize()
            assert "list_todos" in [t.name for t in (await session.list_tools()).tools]
            result = await session.call_tool("list_todos",{})
            if result.isError:
                raise RuntimeError(result.content)
            print(result.structuredContent["result"])

if __name__ == "__main__":
    asyncio.run(check())
