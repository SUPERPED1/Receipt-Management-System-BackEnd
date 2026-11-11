from app.core.config import DB_NAME, DB_PASS, DB_PORT, DB_SERVER, DB_USER
from mysql.connector import pooling

receipts_pool = pooling.MySQLConnectionPool(
    pool_name="receipt_pool",
    pool_size=2,
    pool_reset_session=True,

    host=DB_SERVER,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
)

def get_database_connection():
    return receipts_pool.get_connection()