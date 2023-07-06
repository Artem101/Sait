import json

from aiohttp import web
import aiohttp_jinja2
from sqlalchemy.orm import sessionmaker

from Mydatabase.customization import engine
from Mydatabase.db_user import Post, Comment, User

routes = web.RouteTableDef()
session_factory = sessionmaker(bind=engine)

@routes.get('/login')
@aiohttp_jinja2.template('login.html')
async def login(request):
    return {}


@routes.post('/login')
async def post_login(request):
    data = await request.post()
    name = data.get('name')
    password = data.get('password')
    redirect_url = request.cookies.get('redirect_url') or '/'

    if not name:
        return web.Response(text='Please provide a name.')

    if redirect_url == "/chat_gtp":
        with session_factory() as session:
            user = session.query(User).filter_by(name=name,password=password).first()
            if not user:
                return web.Response(text='Invalid password.')

            redirect_url = request.cookies.get('redirect_url') or '/'
            response = web.HTTPFound(redirect_url)
            response.set_cookie('user_id', str(user.id))
            response.set_cookie('is_authenticated', 'True')
            response.set_cookie('name', name)
            response.del_cookie('redirect_url')

            return response

    elif redirect_url == "/forum":
        with session_factory() as session:
            user = session.query(User).filter_by(name=name, password=password).first()
            if not user:
                return web.Response(text='Invalid password.')

            post_data = request.cookies.get('post_data')
            if post_data:
                post_data = json.loads(post_data)
                title = post_data.get('title')
                text = post_data.get('content')
                descp = post_data.get('description')

                post = session.query(Post).filter_by(content=text).first()

                if not post:
                    new_post = Post(title=title, content=text, description=descp, post_creator_name=name)
                    session.add(new_post)
                    session.commit()

                    # Increment num_posts for the associated user
                    user.num_posts += 1
                    session.commit()

                    last_id = session.query(Post).order_by(Post.id.desc()).first().id
                    response = web.HTTPFound(f'/post/{last_id}')
                    response.set_cookie('numpost', str(user.num_posts))
                    response.del_cookie('post_data')
                    return response
                else:
                    return web.Response(text=f"Такая тема уже есть!")

    elif redirect_url.startswith("/post/"):
        with session_factory() as session:
            user = session.query(User).filter_by(name=name, password=password).first()
            if not user:
                return web.Response(text='Invalid password.')

            response = web.HTTPFound(redirect_url)
            response.set_cookie('user_id', str(user.id))
            response.set_cookie('is_authenticated', 'True')
            response.set_cookie('name', name)
            response.del_cookie('redirect_url')

            comment_text = request.cookies.get('comment_text')
            if comment_text:
                post_id = redirect_url.split("/")[2]
                new_comment = Comment(author=name, text=comment_text, post_id=post_id)
                session.add(new_comment)
                session.commit()
                response.del_cookie('comment_text')

            return response