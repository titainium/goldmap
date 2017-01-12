#!/usr/bin/env python

"""
The basic web crawler for jin10.com.

Titainium Deng
knifewolf@126.com
"""

import asyncio
import json

from pyquery import PyQuery as pq

import aiohttp
import asyncpg
import uvloop

from config import JINTEN_LOGGER

async def fetch(session, url):
    try:
        with aiohttp.Timeout(10, loop = session.loop):
            async with session.get(url) as response:
                return await response.text()
    except Exception:
        JINTEN_LOGGER.exception("messages")

async def main(loop):
    try:
        conn_pool = await asyncpg.create_pool(database = 'webCrawler', user = 'titainium')

        async with conn_pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetchrow("""select * from target_sites where id = 1""")
        
        async with aiohttp.ClientSession(loop = loop) as session:
            html = await fetch(session, result['target_url'] + result['relay_point'])
        
        insect_food = pq(html, parser = 'html')
        raw_material = json.dumps({'raw': insect_food(".jin-news-article").html()})
        semi_finished_goods = json.dumps({'semi': insect_food(".jin-news-article").text()})
        
        async with conn_pool.acquire() as connection:
            async with connection.transaction():
                result = await connection. execute("""INSERT INTO jin10.insect_foods(raw_material, semi_finished_goods) VALUES ($1, $2);""", raw_material, semi_finished_goods)
    except Exception:
        JINTEN_LOGGER.exception("messages")

if __name__ == '__main__':
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(loop))