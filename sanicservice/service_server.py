import asyncio

import uvloop

from sanic import Sanic
from wallstreetCNCrawlerService import wallstreetCN_bp

app = Sanic(__name__)
app.blueprint(wallstreetCN_bp)

asyncio.set_event_loop(uvloop.new_event_loop())

server = app.create_server(host = '0.0.0.0', port = 7000, debug = True)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(server)

try:
    loop.run_forever()
except:
    loop.stop()
