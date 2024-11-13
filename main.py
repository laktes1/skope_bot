import asyncio
import os

from clients.tg import TgClient


async def run_echo():
   c = TgClient(os.getenv("BOT_TOKEN"))
   print(await c.get_updates(offset=0, timeout=5))


if __name__ == "__main__":
   asyncio.run(run_echo())