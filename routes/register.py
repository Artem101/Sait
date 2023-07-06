from aiohttp import web
import aiohttp_jinja2
from sqlalchemy.orm import sessionmaker

from Mydatabase.customization import engine
from Mydatabase.db_user import User
from routes.mail import message_mail
routes = web.RouteTableDef()
session_factory = sessionmaker(bind=engine)

@routes.get('/register')
@aiohttp_jinja2.template('register.html')
async def register(request):
    return {}

@routes.post('/register')
async def do_register(request):
    data = await request.post()
    username = data.get('email')
    password = data.get('password')

    if not (username and password):
        return web.HTTPBadRequest(text='Необходимо заполнить все поля')

    session = session_factory()
    user = session.query(User).filter_by(name=username).first()
    if not user:
        new_user = User(code=0)
        new_user.name = username
        new_user.password = password
        session.add(new_user)
        session.commit()
        user_id = str(new_user.id)  # Преобразуем id в строку
        session.close()
        print(user_id)

        # Сохраняем данные сессии в куки
        response = web.HTTPFound('/forum')
        response.set_cookie('user_id', str(user_id))
        response.set_cookie('name', username)
        response.set_cookie('is_authenticated', 'True')

        return response
    else:
        return web.HTTPUnauthorized(text='Пользователь уже зарегистрирован')