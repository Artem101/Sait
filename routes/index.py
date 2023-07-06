from aiohttp import web
import aiohttp_jinja2

routes = web.RouteTableDef()

# главная страница
@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}