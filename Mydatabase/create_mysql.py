import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='2334'
)

with conn.cursor() as cursor:
    cursor.execute("CREATE DATABASE IF NOT EXISTS worlditco")

conn.close()

