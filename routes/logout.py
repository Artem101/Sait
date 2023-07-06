from aiohttp import web
from aiohttp_session import get_session

routes = web.RouteTableDef()

@routes.get('/logout')
async def clear_session(request):
    response = web.HTTPFound('/forum')
    response.del_cookie('user_id')
    response.del_cookie('name')
    response.del_cookie('is_authenticated')
    response.del_cookie('numpost')
    session = await get_session(request)
    session.clear()
    return response