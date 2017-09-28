import sys

from sanic import Blueprint
from sanic.response import json

import aiohttp

from service_config import SANIC_LOGGER

sys.path.append("..")
from newscrawler.wallstreetcnCrawler import WallStreetCNCrawler
#from goldmap.newscrawler.wallstreetcnCrawler import WallStreetCNCrawler

wallstreetCN_bp = Blueprint('wallstreetCNCrawlerService')

@wallstreetCN_bp.route('/')
async def bp_root(request):
    try:
        wall_street_cn = WallStreetCNCrawler()
    
        async with aiohttp.ClientSession() as client:
            base_url, start_id = await wall_street_cn.get_site()
        
            for idx in range(10):
                status, html = await wall_street_cn.fetch_html(client, base_url, start_id, idx)
            
                if status == 200 and html:
                    title_with_tags, title_text, content_with_tags, content_text = await wall_street_cn.get_html(html)
                
                    if title_text and content_text:
                        await wall_street_cn.save_html(title_with_tags, title_text, content_with_tags, content_text, start_id, idx)
        
        return json({'wallstreetcnCrawler': 'Catch data OK!'})
    except:
        SANIC_LOGGER.exception("wallstreetcnService.bp_root")
        
        return json({'wallstreetcnCrawler': 'Catch data Fail!'})
