# -*- coding: utf-8 -*-
import multiprocessing
import ssl
import aiohttp_autoreload
from aiohttp import web
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from Mydatabase.customization import engine
from Mydatabase.db_user import Base, User
from main import app, session_factory
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
metadata = MetaData()

def start_http_server():
    web.run_app(app, host='185.38.84.93', port=80)


def start_https_server():
    Base.metadata.create_all(engine)
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain('.certs/cert.txt', '.certs/pk.txt')
    ssl_context.load_verify_locations('.certs/Intermediate-1.crt')  # добавляем промежуточный сертификат
    web.run_app(app, host='185.38.84.93', port=443, ssl_context=ssl_context)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    web.run_app(app)

    """
    Session = sessionmaker(bind=engine)

    # создаем новую сессию
    session = Session()
    aiohttp_autoreload.start()

    http_server = multiprocessing.Process(target=start_http_server)
    https_server = multiprocessing.Process(target=start_https_server)

    http_server.start()
    https_server.start()

    http_server.join()
    https_server.join()
    """


