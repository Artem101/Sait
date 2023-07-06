from markupsafe import escape

from aiohttp import web
import aiohttp_jinja2
from sqlalchemy.orm import sessionmaker

from Mydatabase.customization import engine
from Mydatabase.db_user import Post, Comment
from function import textprocessing

routes = web.RouteTableDef()
session_factory = sessionmaker(bind=engine)
@routes.get('/post/{post_id}')
@aiohttp_jinja2.template('post.html')
async def handle(request):
    post_id = request.match_info['post_id']

    # Проверяем, что post_id является числом
    if not post_id.isdigit():
        raise web.HTTPBadRequest(text='No post')

    with session_factory() as session:
        # Получаем объект поста из базы данных по его id
        post = session.query(Post).filter(Post.id == post_id).first()
        if not post:
            response = web.FileResponse('templates/404.html')
            return response




        # Получаем информацию о просмотре поста из кук
        views_cookie_name = f'views_{post_id}'
        views_cookie_value = request.cookies.get(views_cookie_name, '')
        if views_cookie_value != '1':
            # Увеличиваем счетчик просмотров поста на 1
            post.views += 1
            session.add(post)
            session.commit()

            # Сохраняем информацию о просмотре поста в куках
            response = web.HTTPFound(f'/post/{post_id}')
            response.set_cookie(views_cookie_name, '1')
            return response

        # Получаем все комментарии для данного поста из базы данных
        comments = session.query(Comment).filter(Comment.post_id == post_id).all()
        comment_data = [{'text': escape(textprocessing(comment.text)).replace('<p>', '').replace('</p>', ''), 'author': escape(comment.author).replace('<p>', '').replace('</p>', ''), 'date': comment.date} for comment in comments]

        return aiohttp_jinja2.render_template('post.html', request, {
            'title': post.title,
            'text': escape(textprocessing(post.content)).replace('<p>', '').replace('</p>', ''),
            'views': post.views,
            'id': post.id,
            'likes': post.like,
            'comments': comment_data,
            'description': escape(post.description).replace('<p>', '').replace('</p>', ''),
        })
