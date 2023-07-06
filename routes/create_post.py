import json

import aiohttp_jinja2
from aiohttp import web
from sqlalchemy.orm import sessionmaker

from Mydatabase.customization import engine
from Mydatabase.db_user import  Post, User

routes = web.RouteTableDef()
session_factory = sessionmaker(bind=engine)

@routes.post("/create_post")
async def create_post(request):
    data = await request.post()
    user_id = request.cookies.get('user_id')
    title = data.get('title')
    text = data.get('text')
    descp = data.get('description')

    if not (title and text and descp):
        return web.HTTPBadRequest(text='Необходимо заполнить все поля')

    with session_factory() as session:
        if not user_id:
            # If user is not authenticated, store the post in a cookie
            post_data = {'title': title, 'content': text, 'description': descp}
            response = web.HTTPFound('/login')
            response.set_cookie('post_data', json.dumps(post_data))
            response.del_cookie('redirect_url')
            response.set_cookie('redirect_url', '/forum')
            return response

        # If user is authenticated, create the post in the database
        user = session.query(User).filter_by(id=user_id).first()
        name = user.name
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

            # Check for post data in cookie
            post_data_cookie = request.cookies.get('post_data')
            if post_data_cookie:
                post_data = json.loads(post_data_cookie)
                new_post = Post(title=post_data['title'], content=post_data['content'], description=post_data['description'], post_creator_name=name)
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

@routes.get("/create_post")
@aiohttp_jinja2.template('create_post.html')
async def show_create_post(request):
    return {}