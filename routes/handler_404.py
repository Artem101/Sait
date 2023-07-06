import aiohttp_jinja2
from aiohttp import web


routes = web.RouteTableDef()

@web.middleware
async def handle_404(request, handler):
    try:
        response = await handler(request)
    except web.HTTPException as ex:
        if ex.status == 404:
            response = aiohttp_jinja2.render_template('404.html', request, {})
            response.set_status(404)
            return response
        raise
    if response.status == 404:
        response = aiohttp_jinja2.render_template('404.html', request, {})
        response.set_status(404)
        return response
    return response