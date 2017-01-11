#!/usr/bin/env python

"""
The basic web crawler for jin10.com.

Titainium Deng
knifewolf@126.com
"""

import asyncio
import logging

import aiohttp
import uvloop

from config import *

async def fetch(session, url):
    try:
        with aiohttp.Timeout(10, loop = session.loop):
            async with session.get(url) as response:
                return await response.text()
    except Exception as e:
        JINTEN_LOGGER.exception("messages")

async def main(loop):
    try:
        async with aiohttp.ClientSession(loop = loop) as session:
            html = await fetch(session, 'https://news.jin10.com/article/11412')

            with open('sample.html', 'w') as html_file:
                html_file.write(html)
    except Exception as e:
        JINTEN_LOGGER.exception("messages")

if __name__ == '__main__':
    loop = uvloop.new_event_loop()
    
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(loop))