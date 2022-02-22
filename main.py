from models import *
from fastapi import FastAPI
from routers import users, items
from internal import admin

app = FastAPI()
setup_db()


app.include_router(users.router)
app.include_router(items.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
