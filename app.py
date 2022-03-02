import logging
import filters, middlewares, handlers
from aiogram import executor
from loader import dp, db, scheduler

from utils.notify_admins import on_startup_notify
from utils.parsers.VK_parser import parsing_vk


def schedule_jobs():
    scheduler.add_job(parsing_vk, 'interval', seconds=10)

async def on_startup(dp):
    logging.info("Создаем подключение к базе данных")
    await db.create()

    #await db.drop_users()
    #await db.drop_vk_posts()

    logging.info("Создаем таблицу пользователей")
    await db.create_table_users()
    logging.info("Готово.")
    logging.info("Создаем таблицу Парсера")
    await db.create_table_vkposts()
    logging.info("Готово.")
    await on_startup_notify(dp)
    schedule_jobs()


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
