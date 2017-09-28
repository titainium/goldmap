#!/usr/bin/env python
from datetime import date

import asyncio

from bs4 import BeautifulSoup
from pyArango import connection

import aiohttp
import uvloop

from config import WS_LOGGER

__all__ = ['wallStreetCNCrawler']

class WallStreetCNCrawler:
    """
    A Class of a web crawler to catch data from wallstreetcn.com
    """
    
    def __init__(self):
        self.__conn = connection.Connection(username = 'goldmapAdmin', password = 'openSUSE2000$')
        self.__db = self.__conn['goldmapDevDB']
    
    async def fetch_html(self, client, url, start, offset):
        try:
            site_address = ''.join([url, str(start + offset)])
        
            with aiohttp.Timeout(10, loop = client.loop):
                async with client.get(site_address) as resp:
                    return resp.status, await resp.text()
        except:
            WS_LOGGER.exception("wallstreetcn.fetch_html_message")

    async def get_html(self, html):
        try:
            soup = BeautifulSoup(html, 'lxml')
            target_title = soup.title
            target_content = soup.find('div', attrs = {'class': 'article__content'})
        
            if target_title and target_content:
                title_html = target_title.prettify()
                title_text = target_title.text
                content_html = target_content.prettify()
                content_text = target_content.text
    
                return (title_html, title_text, content_html, content_text)
            else:
                return (None, None, None, None)
        except:
            WS_LOGGER.exception("wallstreetcn.get_html_message")

    async def get_site(self):
        try:
            site_doc = self.__db.fetchDocument('fin_sites/wallstreetcn')
        
            return site_doc['crawler_url'], site_doc['crawler_start_id']
        except:
            WS_LOGGER.exception("wallstreetcn.get_site_message")

    async def save_html(self, title_html, title_text, content_html, content_text, start_id, idx):
        try:
            article_coll = self.__db['fin_articles']
            article_doc = article_coll.createDocument()
            article_doc['title'] = title_text
            article_doc['title_html'] = title_html
            article_doc['content'] = content_text
            article_doc['content_html'] = content_html
            article_doc['idx'] = start_id + idx
        
            article_doc.save()
        
            site_doc = self.__db.fetchDocument('fin_sites/wallstreetcn')
            site_doc['crawler_start_id'] = start_id + idx
        
            site_doc.save()
        except:
            WS_LOGGER.exception("wallstreetcn.save_html_message")

async def main(loop):
    try:
        wall_street_cn = WallStreetCNCrawler()
    
        async with aiohttp.ClientSession(loop=loop) as client:
            base_url, start_id = await wall_street_cn.get_site()
        
            for idx in range(10):
                status, html = await wall_street_cn.fetch_html(client, base_url, start_id, idx)
            
                if status == 200 and html:
                    title_with_tags, title_text, content_with_tags, content_text = await wall_street_cn.get_html(html)
                
                    if title_text and content_text:
                        await wall_street_cn.save_html(title_with_tags, title_text, content_with_tags, content_text, start_id, idx)
    except:
        WS_LOGGER.exception("wallstreetcn.main_message")

if __name__ == '__main__':
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(loop))
