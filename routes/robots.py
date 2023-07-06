from aiohttp import web


routes = web.RouteTableDef()

@routes.get("/robots.txt")
async def show_favicon(request):
    file_path = './robots.txt'
    return web.FileResponse(file_path)