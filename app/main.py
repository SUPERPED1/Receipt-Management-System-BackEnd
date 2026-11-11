from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import customers, menus, companies, banks, bills
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(customers.router)
app.include_router(menus.router)
# app.include_router(companies.router)
app.include_router(banks.router)
# app.include_router(bills.router)
    
# app.mount("/", StaticFiles(directory=r"templates", html=True), name="frontend")