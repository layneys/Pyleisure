import asyncio
import uvicorn

from app.bot import main as run_bot
from app.main import app

async def start_server():
    config = uvicorn.Config(
        app=app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()

async def run_all():
    bot_task = asyncio.create_task(run_bot())
    server_task = asyncio.create_task(start_server())

    done, pending = await asyncio.wait(
        [bot_task, server_task],
        return_when=asyncio.FIRST_COMPLETED
    )

if __name__ == "__main__":
    asyncio.run(run_all())