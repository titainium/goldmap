#!/usr/bin/env python

"""
The basic web crawler for jin10.com.

Titainium Deng
knifewolf@126.com
"""

from datetime import date

import asyncio
import json
import os

from pyquery import PyQuery as pq

import aiohttp
import asyncpg
import uvloop

from config import JINTEN_LOGGER

async def fetch_html(session, url):
    try:
        with aiohttp.Timeout(10, loop = session.loop):
            async with session.get(url) as response:
                return await response.text()
    except Exception:
        JINTEN_LOGGER.exception("jinten.fetch_html_messages")

async def fetch_image(session, url):
    try:
        with aiohttp.Timeout(10, loop = session.loop):
            async with session.get(url) as response:
                return await response.read()
    except Exception:
        JINTEN_LOGGER.exception("jinten.fetch_image_messages")

async def main(loop):
    try:
        conn_pool = await asyncpg.create_pool(database = 'webCrawler', user = 'titainium')

        async with conn_pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetchrow("""select * from target_sites where id = 1""")
        
        async with aiohttp.ClientSession(loop = loop) as session:
            relay_point = result['relay_point']
            html = await fetch_html(session, result['target_url'] + relay_point)
            insect_food = pq(html, parser = 'html')
            raw_material = json.dumps({'title': insect_food(".jin-news-article_h").html(),
                                       'description': insect_food(".jin-news-article_description").html(),
                                       'content': insect_food(".jin-news-article_content").html()})
            semi_finished_goods = json.dumps({'semi': insect_food(".jin-news-article_content").text()})
            images = insect_food(".jin-news-article_content").find("img")
            download_files = []

            if not os.path.isdir(os.path.join(os.getcwd(), "download_imgs", "jin10", date.today().isoformat())):
                os.makedirs(os.path.join(os.getcwd(), "download_imgs", "jin10", date.today().isoformat()))
            
            for img in images:
                with open(os.path.join(os.getcwd(),
                                       "download_imgs",
                                       "jin10",
                                       date.today().isoformat(),
                                       img.attrib["src"].split("/")[-1]),
                          "wb") as image_file:
                    image_file.write(await fetch_image(session, img.attrib["src"]))
                    download_files.append((os.path.join(os.getcwd(),
                                                        "download_imgs",
                                                        "jin10",
                                                        date.today().isoformat(),
                                                        img.attrib["src"].split("/")[-1]),
                                           img.attrib["src"]))

        async with conn_pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.execute("""INSERT INTO jin10.insect_foods(raw_material,
                                                                                     semi_finished_goods,
                                                                                     raw_id)
                                                     VALUES ($1, $2, $3);""",
                                                  raw_material,
                                                  semi_finished_goods,
                                                  relay_point
                                                  )
                raw_id = await connection.fetchrow("""SELECT id FROM jin10.insect_foods WHERE raw_id = $1;""", relay_point)
        
        async with conn_pool.acquire() as connection:
            async with connection.transaction():
                for img_file in download_files:
                    img_result = await connection.execute("""INSERT INTO jin10.complementary_foods(image_name,
                                                                                                   image_address,
                                                                                                   stored_path,
                                                                                                   food_id)
                                                             VALUES ($1, $2, $3, $4)""",
                                                          img_file[0].split("/")[-1],
                                                          img_file[1],
                                                          img_file[0],
                                                          raw_id['id'])
    except Exception:
        JINTEN_LOGGER.exception("messages")

if __name__ == '__main__':
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(loop))