from sqlalchemy import create_engine, MetaData, text

from Mydatabase import db_user

DB_NAME = 'worlditco'
PASSWORD = '2334'
engine = create_engine(f'mysql+pymysql://root:{PASSWORD}@localhost:3306/{DB_NAME}')
'''
with engine.connect() as conn:
    # Удаление базы данных
    conn.execute(text("DROP DATABASE IF EXISTS it_forum"))
'''