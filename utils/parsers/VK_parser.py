import logging
import aiohttp
from aiogram import types
from aiogram.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton

from data.config import admins
from keyboards.inline.callback_datas import upload_callback
from loader import dp
from utils.db_api.postgresql import Database



async def parsing_vk():
    db = Database()
    await db.create()
    vk_source = await db.get_last_known_id()
    list_vk_sources = list()
    list_last_known_id = list()
    for i in vk_source:
        list_last_known_id.append(list(i)[0])
        list_vk_sources.append(list(i)[1])
    print(list_vk_sources)
    print(list_last_known_id)
    is_new = False

    for j in range(len(list_vk_sources)):
        url = f"https://api.vk.com/method/wall.get?domain={list_vk_sources[j]}&count=2&filter=owner&access_token=ca7420e9ca7420e9ca7420e9dcca02c222cca74ca7420e9aa3a46e22e24f4fcb477dd99&v=5.130"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                response = await resp.json()
                print(response)
                logging.info('')
                id = str(response["response"]["items"][1]["id"])
                if response["response"]["items"][1]["marked_as_ads"] == 1:
                    continue
                attachments = response["response"]["items"][1]["attachments"]
                if id in list_last_known_id:
                    continue
                img_list = []
                img_count = 1
                for attach in attachments:
                    try:
                        photo = attach["photo"]["sizes"][-1]["url"]
                    except:
                        continue
                    async with session.get(photo) as r:
                        print(r)
                        res = await r.read()
                    with open(f"utils\\parsers\\media\\{list_vk_sources[j]}\\media{img_count}.jpg", "wb") as file:
                        file.write(res)
                        img_list.append(f"media{img_count}.jpg")
                        print(f"Downloaded {img_count}")
                        logging.info(f"получено фото {photo}")
                        print(photo)
                        img_count += 1
                await db.update_last_known_id(id, list_vk_sources[j])
                is_new = True
                print(img_list)
                break
    if not is_new:
        print("Новых не найдено")
        logging.info("Новых не найдено")
        return
    photo = InputFile(f"utils\parsers\media\{list_vk_sources[j]}\media{img_count-1}.jpg")
    print(f"-----------------------{photo}")
    await check_upload(photo, img_count, list_vk_sources[j])

async def upload(img_count, source):
    album = types.MediaGroup()
    for pic in range(1, img_count):
        if pic == img_count-1:
            photo = InputFile(f"utils\parsers\media\{source}\media{pic}.jpg")
            album.attach_photo(
                photo=photo,
                caption="подготовленный текст"
            )
        else:
            photo = InputFile(f"utils\parsers\media\{source}\media{pic}.jpg")
            album.attach_photo(
                photo=photo,
            )
    await dp.bot.send_media_group("@tsdfe", album)

async def check_upload(photo, img_count, source):
    msg = await dp.bot.send_photo(int(admins[0]), photo,
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                      [
                                          InlineKeyboardButton(
                                              text="OK",
                                              callback_data=upload_callback.new(img_count=img_count,
                                                                                source=source)

                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text="Отмена",
                                              callback_data="cancel"
                                          )
                                      ]
                                  ])
                                  )


    # if link1 in list_doms:
    #     print("Я ебучий гений")
    #     print(re.findall(r'\w/(.+)', link)[0])
    #     print(re.findall(r'\w/(.+)[?]', link)[0])
