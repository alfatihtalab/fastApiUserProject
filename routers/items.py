from dependencies import *
from models.models import *
from sqlmodel import select, update
from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},)


@router.get("/")
async def read_items():
    """Get user by id"""
    with Session(engine) as session:
        statement = select(Item)
        results = session.exec(statement)
        items_match = results.all()
        return items_match


@router.get("/{item_id}")
async def read_item(item_id: str):
    with Session(engine) as session:
        statement = select(Item).where(Item.id == item_id)
        results = session.exec(statement)
        item = results.first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item.dict()


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str, item: Item):
    with Session(engine) as session:
        statement = select(Item).where(Item.id == item_id)
        results = session.exec(statement)
        item_db = results.first()
        if item_db:
            # item_db = {"id": item_id, **item.dict()}
            update(Item, Item.id == item_id, item).execute()


        else:
            raise HTTPException(
                status_code=403, detail="You can only update the item: plumbus"
            )

    return {"item_id": item_id, "name": "The great Plumbus"}