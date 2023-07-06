from aiohttp import web
import aiohttp_jinja2
from sqlalchemy.orm import sessionmaker

from Mydatabase.customization import engine
from Mydatabase.db_user import ChatGtp
from function import textprocessing, chatgtp

routes = web.RouteTableDef()
session_factory = sessionmaker(bind=engine)

@routes.get('/chat_gtp')
@aiohttp_jinja2.template('chat_gtp.html')
async def get_chat_gtp(request):
    user_id = request.cookies.get('user_id')
    is_authenticated = request.cookies.get('is_authenticated')
    name = request.cookies.get('name')


    with session_factory() as session:
        last_requests = session.query(ChatGtp).filter_by(user_id=user_id).order_by(ChatGtp.id).limit(20).all()
        data = [{'text': textprocessing(table.message_text), 'query': table.query} for table in last_requests]

    context = {'text': data, 'name': name}
    return aiohttp_jinja2.render_template('chat_gtp.html', request, context)
@routes.post('/chat_gtp')
@aiohttp_jinja2.template('chat_gtp.html')
async def post_chat_gtp(request):
    data = await request.post()
    name = request.cookies.get('name')

    if not name:
        response = web.HTTPFound('/login')
        response.set_cookie('redirect_url', '/chat_gtp')
        return response

    user_id = request.cookies.get('user_id')
    is_authenticated = True
    text = data.get('chattext')
    chatgtp(text, user_id)

    return web.HTTPFound('/chat_gtp')
