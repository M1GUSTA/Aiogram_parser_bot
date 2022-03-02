import logging
import re

import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.types import CallbackQuery, update

from data.config import admins
from filters.private_chat import IsPrivate
from keyboards.inline.admin_buttons import admin_choice, source_keyboard, another_try
from keyboards.inline.callback_datas import db_callback
from loader import dp, db
from states.admin import Parsing
from utils.parsers.VK_parser import upload


@dp.message_handler(IsPrivate(), CommandStart(), user_id=admins)
async def admin_chat_secret(message: types.Message):
    await message.answer(text="Это сообщение для взора избранных. \n"
                              "Что вы хотите",
                         reply_markup=admin_choice)

@dp.message_handler(Command("anim"),user_id=admins)
async def send_animation(message: types.Message):
    await dp.bot.send_animation(chat_id=message.from_user.id,
                                 animation="https://video.twimg.com/tweet_video/DvinM9nXQAEqAZG.mp4",
                                 caption="heh")


@dp.callback_query_handler(db_callback.filter(db_name="VK_posts"))
async def getting_the_source(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f"callback_data = {call.data}")
    logging.info(f"callback_data dict = {callback_data}")
    await call.message.answer("Какой источник вы хотите добавить",
                              reply_markup=source_keyboard)

    await Parsing.getting_source.set()


@dp.message_handler(state=Parsing.getting_source)
async def link_check(message: types.Message, state: FSMContext):
    link = message.text
    await state.update_data(link=link)
    tmp = await db.select_all_domains()
    print(tmp)
    list_doms = list()
    for i in tmp:
        list_doms.append(list(i)[0])
    print(list_doms)
    try:
        link1 = re.findall(r'//(.+)/', link)[0]
    except:
        await message.answer(text="Этот источник не может быть добавлен",
                             reply_markup=another_try)

    if link1 in list_doms:
        wall_name = re.findall(r'\w/(.+)', link)[0]
        print(wall_name)
        url = f"https://api.vk.com/method/wall.get?domain={wall_name}&count=2&filter=owner&access_token=ca7420e9ca7420e9ca7420e9dcca02c222cca74ca7420e9aa3a46e22e24f4fcb477dd99&v=5.130"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                response = await resp.json()
                print(response)
    else:
        print("Я ебучий лох")
        return
    await message.answer(link)


@dp.callback_query_handler(text_contains="upload")
async def accept_upload_post(call: CallbackQuery,):
    await call.answer(cache_time=60)
    callback_data = re.split(":", call.data)
    source = callback_data[2]
    img_count = int(callback_data[1])
    await upload(img_count, source)
