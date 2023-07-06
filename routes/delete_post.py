from aiohttp import web
from sqlalchemy.orm import sessionmaker

from Mydatabase.customization import engine
from Mydatabase.db_user import Comment, Like, Post, User

routes = web.RouteTableDef()
session_factory = sessionmaker(bind=engine)

@routes.get("/delete/{post_id}")
async def delete_post(request):
    post_id = int(request.match_info['post_id'])

    with session_factory() as session:
        # Удаляем все комментарии для данного поста
        session.query(Comment).filter(Comment.post_id == post_id).delete()

        # Удаляем все лайки для данного поста
        session.query(Like).filter(Like.post_id == post_id).delete()

        # Удаляем все просмотры для данного поста
        response = web.HTTPFound("/forum")
        response.del_cookie(f"views_{post_id}")

        # Получаем всех пользователей, связанных с удаляемым постом
        user_ids = set()
        for model_class in (Comment, Like):
            q = session.query(model_class).filter(model_class.post_id == post_id)
            for obj in q:
                user_ids.add(obj.user_id)

        # Удаляем всех пользователей, связанных с удаляемым постом
        session.query(User).filter(User.id.in_(user_ids)).delete(synchronize_session=False)

        # Удаляем удаляемый пост
        session.query(Post).filter(Post.id == post_id).delete()

        # Сохраняем изменения
        session.commit()

    return web.HTTPFound("/forum")
