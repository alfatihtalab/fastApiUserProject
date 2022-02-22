from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import select

from dependencies import *
from models.models import *

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}, )


# get all users
@router.get("/", dependencies=[Depends(get_token_header)], )
async def read_users():
    """Get all users from database"""
    with Session(engine) as session:
        statement = select(User)
        results = session.exec(statement)
        if not results:
            raise HTTPException(status_code=404, detail="No users")
        return [user for user in results]


@router.get("/{user_id}")
async def read_user(user_id: int):
    """Get user by id"""
    with Session(engine) as session:
        statement = select(User)
        results = session.exec(statement)
        user_match = {}
        for user in results:
            if user.id == user_id:
                user_match = user.dict()
        return user_match


@router.post("/signup/")
async def add_user(user: User):
    """Create new user"""
    users = await read_users()
    users_emails = [u.email for u in users]
    user_dict = user.dict()
    if user.account_id in [1001, 1002, 1003] and user.email not in users_emails:
        try:
            user.insert()
        except:
            return {"message": "error in transaction"}
        return user_dict
    else:
        raise HTTPException(status_code=404, detail="Can not added")


@router.patch("/{user_id}")
async def update_user(user_id: int, user: User):
    """Update user by id"""
    # result = {"id": id, **user.dict()}
    # with Session(engine) as session:
    #     statement = select(User).where(User.id == id)
    #     results = session.exec(statement)
    #     updated_user = results.one()
    #     updated_user.name = user.name
    #     updated_user.password = user.password
    #     session.add(updated_user)
    #     session.commit()
    #     session.refresh(updated_user)
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


###

@router.delete("/user/{user_id}")
async def delete_user(user_id: int):
    with Session(engine) as session:
        statement = select(User).where(User.id == user_id)

        results = session.exec(statement)
        if not results:
            raise HTTPException(status_code=404, detail="No users")

        user = results.one()

        session.delete(user)
        session.commit()

        return await read_users()


@router.get("/user/signin/", dependencies=[Depends(get_query_token)])
async def login(email: str, password: str):
    try:
        with Session(engine) as session:
            statement = select(User).where(email == email)
            result = session.exec(statement)
            if result:
                if result.first().password == password:
                    print('welcome')
                else:
                    print('wrong password')
            else:
                print('please register first')
    except:
        raise HTTPException(status_code=404, detail="No users")
