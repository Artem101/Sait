from aiohttp import web


routes = web.RouteTableDef()

@routes.get("/favicon2.png")
async def show_favicon(request):
    file_path = 'static/./favicon2.png'
    return web.FileResponse(file_path)
