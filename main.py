# -*- coding: utf-8 -*-

import base64
import aiohttp_jinja2
import jinja2

from aiohttp import web
from aiohttp_session import setup,  session_middleware
from pathlib import Path

from aiohttp_session.cookie_storage import EncryptedCookieStorage

from sqlalchemy.orm import sessionmaker

from Mydatabase.customization import engine

from config import key

BASE_DIR = Path(__file__).parent

encoded_key = base64.urlsafe_b64encode(key.encode())
session_storage = EncryptedCookieStorage(encoded_key.decode())

routes = web.RouteTableDef()
session_factory = sessionmaker(bind=engine)
from routes.index import routes as index
from routes.sitemap import routes as sitemap
from routes.robots import routes as robots
from routes.favicon_ico import routes as favicon
from routes.favicon_png import routes as favicon_png
from routes.handler_404 import handle_404
from routes.chat_gtp import routes as chat_gtp
from routes.get_post import routes as get_post
from routes.delete_post import routes as delete_post
from routes.create_post import routes as create_post
from routes.add_comment import routes as add_comment
from routes.like_post import routes as like_post
from routes.forum import routes as forum
from routes.login import routes as login
from routes.register import routes as register
from routes.mail import routes as mail
from routes.logout import routes as logout



# статические файлы
app = web.Application()
app.add_routes(routes)
app.add_routes(index)
app.add_routes(sitemap)
app.add_routes(robots)
app.add_routes(favicon)
app.add_routes(favicon_png)
app.add_routes(register)
app.add_routes(chat_gtp)
app.add_routes(get_post)
app.add_routes(delete_post)
app.add_routes(create_post)
app.add_routes(add_comment)
app.add_routes(like_post)
app.add_routes(forum)
app.add_routes(login)
app.add_routes(register)
app.add_routes(mail)
app.add_routes(logout)


aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.router.add_static('/static/', path=BASE_DIR / 'static', name='static')
app.middlewares.append(handle_404)
app.middlewares.append(session_middleware(session_storage))
setup(app, session_storage)

