from aiohttp import web


routes = web.RouteTableDef()

@routes.get("/favicon.ico")
async def show_favicon(request):
    file_path = 'static/./favicon.ico'
    return web.FileResponse(file_path)