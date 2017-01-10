#!/usr/bin/env python

"""
The basic web crawler for jin10.com.

Titainium Deng
knifewolf@126.com
"""

import aiohttp
import asyncio
import uvloop

async def fetch(session, url):
    with aiohttp.Timeout(10, loop = session.loop):
        async with session.get(url) as response:
            return await response.text()

async def main(loop):
    async with aiohttp.ClientSession(loop = loop) as session:
        html = await fetch(session, 'https://news.jin10.com/article/11412')

        with open('sample.html', 'w') as html_file:
            html_file.write(html)

if __name__ == '__main__':
    loop = uvloop.new_event_loop()
    
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(loop))