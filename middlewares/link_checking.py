import logging
import re

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from loader import db


class LinkCheck(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        logging.info("1. Pre Process Update")
        logging.info("Следующая точка: ")
        data["middleware_data"] = "Это пройдет до on_post_process_update"
        tmp = await db.select_all_domains()
        print(tmp)
        list_doms = list()
        for i in tmp:
            list_doms.append(list(i)[0])
        print(list_doms)
        if update.message:
            link = update.message.text
            link = re.findall(r'//(.+)/', link)[0]
            if link in list_doms:
                print("Я ебучий гений")
        else:
            print("Я ебучий лох")
            return
