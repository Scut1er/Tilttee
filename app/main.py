import asyncio
import os
from dotenv import load_dotenv
from bot import bot
from config import USE_LOGGING
from logger import setup_logging

load_dotenv()


async def main():
    async with bot:
        if USE_LOGGING:
            setup_logging()
        await bot.start(os.getenv('TOKEN'))


asyncio.run(main())
