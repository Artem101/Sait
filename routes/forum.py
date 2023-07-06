from markupsafe import escape

from aiohttp import web
import aiohttp_jinja2
from sqlalchemy.orm import sessionmaker

from Mydatabase.customization import engine
from Mydatabase.db_user import Post, Comment, User

routes = web.RouteTableDef()
session_factory = sessionmaker(bind=engine)
@routes.get("/forum")
@aiohttp_jinja2.template('forum.html')
async def forum(request):
    user_id = request.cookies.get('user_id')
    name = request.cookies.get('name')
    numpost = request.cookies.get('numpost')

    session = session_factory()
    user = session.query(User).filter_by(id=user_id).first()
    session.close()

    latest_posts = session.query(Post.id, Post.title, Post.post_creator_name, Post.description).order_by(
        Post.id.desc()).limit(10).all()
    post_data = [{'title': escape(post.title), 'id': post.id, 'post_creator_name': escape(post.post_creator_name), 'description': escape(post.description)}
                     for post in latest_posts]
    context = {'user_id': user_id, 'name': escape(name), 'numpost': numpost if numpost else 0, 'column2': post_data}
    return context
