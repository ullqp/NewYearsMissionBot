import asyncio
import os

from aiogram import Bot, Dispatcher

from dotenv import find_dotenv, load_dotenv

from middlewares.db import DataBaseSession
load_dotenv(find_dotenv())

from database.engine import create_db, session_maker  # noqa: E402
from handlers.user import user_router # noqa: E402



bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
dp.include_router(user_router)



async def on_startup(bot):
    await create_db()


async def on_shutdown(bot):
    print('бот лег')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())