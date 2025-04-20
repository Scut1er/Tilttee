import asyncio
import os
from dotenv import load_dotenv
from app.bot import bot
from app.config import USE_LOGGING
from app.logger import setup_logging

load_dotenv()


async def main():
    async with bot:
        if USE_LOGGING:
            setup_logging()
        await bot.start(os.getenv('TOKEN'))


asyncio.run(main())
