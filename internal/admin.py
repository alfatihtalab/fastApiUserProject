from fastapi import APIRouter
from models import *

router = APIRouter(prefix='/admin')


@router.post("/")
async def add_admin(user: User):
    with Session(engine) as session:
        user.account_id = 1001
        session.add(user)
        session.commit()
        session.close()
    return {"admin": "welcome to teapot"}
