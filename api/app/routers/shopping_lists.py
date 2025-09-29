from fastapi import APIRouter, HTTPException
from ..db import get_session
from .. import models, schemas

router = APIRouter(prefix="/shopping-lists", tags=["shopping-lists"])

@router.post("/", response_model=schemas.ShoppingListOut)
def create_list(payload: schemas.ShoppingListCreate):
    with get_session() as db:
        if db.query(models.ShoppingList).filter_by(name=payload.name).first():
            raise HTTPException(400, detail="List already exists")
        lst = models.ShoppingList(name=payload.name)
        db.add(lst)
        db.flush()
        return schemas.ShoppingListOut.model_validate(lst)

@router.get("/", response_model=list[schemas.ShoppingListOut])
def list_lists():
    with get_session() as db:
        rows = db.query(models.ShoppingList).order_by(models.ShoppingList.id).all()
        return [schemas.ShoppingListOut.model_validate(x) for x in rows]

@router.post("/{lid}/items")
def add_item(lid: int, payload: schemas.ShoppingListItemIn):
    with get_session() as db:
        lst = db.get(models.ShoppingList, lid)
        if not lst:
            raise HTTPException(404, detail="List not found")
        if not db.get(models.Product, payload.product_id):
            raise HTTPException(400, detail="Unknown product")
        db.add(models.ShoppingListItem(list_id=lid, product_id=payload.product_id, quantity=payload.quantity))
        return {"ok": True}

@router.delete("/{lid}")
def delete_list(lid: int):
    with get_session() as db:
        lst = db.get(models.ShoppingList, lid)
        if not lst:
            raise HTTPException(404, detail="Not found")
        db.delete(lst)
        return {"ok": True}
