from aiohttp import web

from sqlalchemy.orm import sessionmaker

from Mydatabase.customization import engine
from Mydatabase.db_user import Post, Comment

routes = web.RouteTableDef()
session_factory = sessionmaker(bind=engine)
@routes.post("/add_comment/{id}")
async def add_comment(request):
    data = await request.post()
    author = request.cookies.get('name')
    text = data.get('comment')
    post_id = request.match_info['id']
    with session_factory() as session:
        post = session.query(Post).filter_by(id=post_id).first()
        if not post:
            return web.HTTPNotFound()
        if not author: # Если пользователь не авторизован
            response = web.HTTPFound('/login') # Редирект на страницу входа
            # Сохранение данных комментария в cookie
            response.set_cookie('comment_author', '', max_age=3600) # Пустое значение для того, чтобы удалить cookie
            response.set_cookie('comment_text', text, max_age=3600)
            response.set_cookie('redirect_url', f'/post/{post_id}', max_age=3600)
            return response
        new_comment = Comment(author=author, text=text, post_id=post_id)
        session.add(new_comment)
        session.commit()

    response = web.HTTPFound(f"/post/{post_id}")
    response.set_cookie('comment_author', author, max_age=3600) # Сохранение имени пользователя в cookie
    response.del_cookie('comment_text') # Удаление данных комментария из cookie
    return response