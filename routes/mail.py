import random

import aiohttp_jinja2
from aiohttp import web
from sqlalchemy.orm import sessionmaker, session
from Mydatabase.customization import engine
import smtplib
from email.message import EmailMessage

from Mydatabase.db_user import User

session_factory = sessionmaker(bind=engine)
routes = web.RouteTableDef()


def message_mail(username,password,request):
    user_id = request.cookies.get('user_id')
    cod = random.randint(100000, 999999)

    session = session_factory()
    user = session.query(User).filter_by(id=user_id).first()
    user.code = cod
    session.commit()
    session.close()

    message = EmailMessage()
    message['Subject'] = 'It форум-Worlditco'
    message['From'] = 'VavArt@worlditco.ru'
    message['To'] = f'{username}'
    message.set_content(f'Ваш проверочный код - {cod}')

    with smtplib.SMTP_SSL('smtp.mail.ru', 465) as server:
        server.login('VavArt@worlditco.ru', 'yzUhyepydBeXCwAdemAh')
        server.send_message(message)
        server.close()


    """
    session = session_factory()
    user = session.query(User).filter_by(name=username).first()
    if not user:
        new_user = User(name=username, password=password)
        session.add(new_user)
        session.commit()
        user_id = new_user.id
        session.close()

        # Сохраняем данные сессии в куки
        response = web.HTTPFound('/forum')
        response.set_cookie('user_id', str(user_id))
        response.set_cookie('name', username)
        response.set_cookie('is_authenticated', 'True')

        return response
    else:
        return web.HTTPUnauthorized(text='Пользователь уже зарегистрирован')
    """

@routes.get('/mail')
@aiohttp_jinja2.template('mail.html')
async def mail(request):
    return {}
@routes.post("/mail")
async def post_mail(request):
    data = await request.post()
    code = data.get("code")
    user_id = request.cookies.get('user_id')
    session = session_factory()
    user = session.query(User).filter_by(id=user_id).first()
    session.close()
    if user.code == "code":
        response = web.HTTPFound('/forum')
        response.set_cookie('is_authenticated', 'True')
        return response
    else:
        return "Код Неверный!"




