

from aiohttp import web

from sqlalchemy.orm import sessionmaker

from Mydatabase.customization import engine
from Mydatabase.db_user import Post, Like

routes = web.RouteTableDef()
session_factory = sessionmaker(bind=engine)
@routes.post("/like_post/{post_id}")
async def like_post(request):
    post_id = request.match_info.get('post_id')
    user_id = request.cookies.get('user_id')

    with session_factory() as session:
        # Check if the user has already liked the post
        existing_like = session.query(Like).filter_by(user_id=user_id, post_id=post_id).first()
        if not existing_like:
            new_like = Like(user_id=user_id, post_id=post_id)
            session.add(new_like)
            session.commit()
            post = session.query(Post).filter_by(id=post_id).first()
            post.like += 1
            session.commit()
        else:
            pass
    # Return a redirect response after the session has been properly closed
    return web.HTTPFound(f"/post/{post_id}")