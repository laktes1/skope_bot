import asyncio
import os

from aiogram import Router
from create_bot import bot, dp, scheduler
from handlers.start import start_router
from handlers.UserHandler import UserHandler


async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()

    # Подключаем стартовый маршрутизатор
    dp.include_router(start_router)

    # Создаём экземпляр UserHandler и добавляем его маршрутизатор
    user_handler = UserHandler(Router())
    dp.include_router(user_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
