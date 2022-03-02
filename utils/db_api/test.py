# import asyncio
# import re
# import redis
# import aiohttp
#
# from utils.db_api.postgresql import Database
#
# loop = asyncio.get_event_loop()
#
# async def parsing_vk():
#     db = Database()
#     await db.create()
#     vk_source = await db.get_last_known_id()
#     list_vk_sources = list()
#     list_last_known_id = list()
#     for i in vk_source:
#         list_last_known_id.append(list(i)[0])
#         list_vk_sources.append(list(i)[1])
#     print(list_vk_sources)
#     print(list_last_known_id)
#     x =1
#     for y in range(x):
#         print(x)
#     for j in range(len(list_vk_sources)):
#         url = f"https://api.vk.com/method/wall.get?domain={list_vk_sources[j]}&count=2&filter=owner&access_token=ca7420e9ca7420e9ca7420e9dcca02c222cca74ca7420e9aa3a46e22e24f4fcb477dd99&v=5.130"
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url) as resp:
#                 response = await resp.json()
#                 print(response)
#                 id = str(response["response"]["items"][1]["id"])
#                 if response["response"]["items"][1]["marked_as_ads"] == 1:
#                     await db.update_last_known_id(id, list_vk_sources[j])
#                     return
#                 attachments = response["response"]["items"][1]["attachments"]
#                 if id in list_last_known_id:
#                     print("-----------------------------------------------")
#                     continue
#                 img_list = []
#                 i = 1
#                 for attach in attachments:
#                     photo = attach["photo"]["sizes"][-1]["url"]
#                     async with session.get(photo) as r:
#                         print(r)
#                         res = await r.read()
#                     with open(f"media/media{i}.jpg", "wb") as file:
#                         file.write(res)
#                         img_list.append(f"media{i}.jpg")
#                         print(f"Downloaded {i}")
#                     i += 1
#                     print(photo)
#                 await db.update_last_known_id(id, list_vk_sources[j])
#                 break
#
#     # r = redis.StrictRedis()
#     # print(r.ping())
#
#
# if __name__ == '__main__':
#     loop.run_until_complete(parsing_vk())

import requests
from bs4 import BeautifulSoup # module for HTML parsing

def get_data():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept - Encoding": "gzip, deflate, br",
        "Accept - Language": "ru - RU, ru; q = 0.9, en - US; q = 0.8, en; q = 0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }

    url = requests.get(url="https://play.google.com/store/search?q=%D1%82%D1%80%D0%B5%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B8,+%D1%84%D0%B8%D1%82%D0%BD%D0%B5%D1%81&c=apps", headers=headers)
    request = BeautifulSoup(url.text, "lxml")
    print(request)

get_data()