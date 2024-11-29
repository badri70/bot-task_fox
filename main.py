import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from router import router
from database import create_all_tables


load_dotenv(dotenv_path=".env")


bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


async def main():
    create_all_tables()
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main=main())