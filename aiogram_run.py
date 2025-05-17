import asyncio

from aiogram.types import BotCommand, BotCommandScopeDefault
from sqlalchemy import create_engine

from db_work import db_session
from create_bot import bot, dp
from db_work.clear_table import TableCleaner
from db_work.db_commands import insert_orders_types
from handlers.start import start_router


async def main():
    db_session.global_init("data/list_of_students.db")
    insert_orders_types()
    dp.include_router(start_router)
    cleaner = TableCleaner(engine=create_engine('sqlite:///list_of_students.db'))
    cleaner.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
