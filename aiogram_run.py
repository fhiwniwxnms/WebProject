import asyncio

from aiogram.types import BotCommand, BotCommandScopeDefault
from data import db_session
from create_bot import bot, dp
from db_work.db_commands import insert_orders_types
from handlers.start import start_router


# from work_time.time_func import send_time_msg

async def set_commands():
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='start_2', description='Старт 2'),
                BotCommand(command='faq', description='Частые вопросы')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    db_session.global_init("list_of_students.db")
    insert_orders_types()
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await set_commands()


if __name__ == "__main__":
    asyncio.run(main())
