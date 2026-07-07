import aiomysql
import mysql.connector as mysql
from app.core import *

db_config = {
    "host":DB_HOST,
    "port":DB_PORT,
    "user":DB_USER,
    "password":DB_PASSWORD,
    "db":DB,
    'autocommit': True
}

db_pool = None

async def create_db_pool():
    global db_pool
    db_pool = await aiomysql.create_pool(
        **db_config,
        minsize=3,
        maxsize=10,
        cursorclass=aiomysql.DictCursor
    )

async def close_db_pool():
    db_pool.close()
    await db_pool.wait_closed()

def sql_sync():
    conn = mysql.connect(
        host="192.168.2.200",
        port=10001,
        user="python",
        password="Python@26201",
        database="receipt_test"
    )
    return conn