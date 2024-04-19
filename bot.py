import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_reader import config
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers import main_handler
from handlers.schedule_handler import send_new_questions

from middlewares.scheduler_middleware import SchedulerMiddleware

from db import get_all_users

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())


async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(main_handler.router)
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.start()
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    users = get_all_users()
    if len(users) != 0:
        for user in users:
            if user[8] != "" and user[9] != "" and user[8] is not None and user[9] is not None:
                if user[9].split(" ")[1] == "нед":
                    scheduler.add_job(send_new_questions, trigger="interval",
                                      week=int(user[9].split(" ")[0]),
                                      kwargs={"user_id": user[1], "bot": bot})
                elif user[9].split(" ")[1] == "дн":
                    scheduler.add_job(send_new_questions, trigger="interval",
                                      day=int(user[9].split(" ")[0]),
                                      kwargs={"user_id": user[1], "bot": bot})
                elif user[9].split(" ")[1] == "ч":
                    scheduler.add_job(send_new_questions, trigger="interval",
                                      hours=int(user[9].split(" ")[0]),
                                      kwargs={"user_id": user[1], "bot": bot})
                elif user[9].split(" ")[1] == "мин":
                    scheduler.add_job(send_new_questions, trigger="interval",
                                      minutes=int(user[9].split(" ")[0]),
                                      kwargs={"user_id": user[1], "bot": bot})
                elif user[9].split(" ")[1] == "сек":
                    scheduler.add_job(send_new_questions, trigger="interval",
                                      seconds=int(user[9].split(" ")[0]),
                                      kwargs={"user_id": user[1], "bot": bot})
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
