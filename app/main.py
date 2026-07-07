from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from app.api.v1 import customers, menus, companies, banks, bills
from app.db.sql_connector import create_db_pool,close_db_pool
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customers.router)
app.include_router(menus.router)
app.include_router(companies.router)
app.include_router(banks.router)
app.include_router(bills.router)

@app.on_event("startup")
async def startup():
    await create_db_pool()

@app.on_event("shutdown")
async def shutdown():
    await close_db_pool()
    
app.mount("/", StaticFiles(directory=r"D:\Every_file\receipt\Receipt_print_project\frontend\dist", html=True), name="frontend")