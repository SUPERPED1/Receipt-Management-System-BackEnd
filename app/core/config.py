import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

DB_SERVER = os.getenv("DB_SERVER")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
