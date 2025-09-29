from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.orm import selectinload
from ..db import get_session
from .. import models, schemas

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.post("/", response_model=schemas.RecipeOut)
def create_recipe(payload: schemas.RecipeCreate):
    with get_session() as db:
        if db.query(models.Recipe).filter_by(name=payload.name).first():
            raise HTTPException(400, detail="Recipe already exists")
        r = models.Recipe(name=payload.name, instructions=payload.instructions or "")
        db.add(r)
        db.flush()
        for it in payload.items:
            if not db.get(models.Product, it.product_id):
                raise HTTPException(400, detail=f"Unknown product {it.product_id}")
            db.add(models.RecipeItem(recipe_id=r.id, product_id=it.product_id, quantity=it.quantity))
        db.flush()
        # ✅ precargar items para que Pydantic no dispare lazy-load tras cerrar sesión
        r = db.query(models.Recipe).options(selectinload(models.Recipe.items)).get(r.id)
        return schemas.RecipeOut.model_validate(r)

@router.get("/", response_model=list[schemas.RecipeOut])
def list_recipes():
    with get_session() as db:
        rows = db.query(models.Recipe).options(selectinload(models.Recipe.items)).order_by(models.Recipe.id).all()
        return [schemas.RecipeOut.model_validate(r) for r in rows]

@router.post("/{rid}/add-to-list")
def add_recipe_to_list(rid: int, list_id: int = Query(...), fail: bool = Query(False)):
    with get_session() as db:
        r = db.query(models.Recipe).options(selectinload(models.Recipe.items)).get(rid)
        if not r:
            raise HTTPException(404, detail="Recipe not found")
        lst = db.get(models.ShoppingList, list_id)
        if not lst:
            raise HTTPException(404, detail="List not found")
        for it in r.items:
            db.add(models.ShoppingListItem(list_id=lst.id, product_id=it.product_id, quantity=it.quantity))
        if fail:
            raise HTTPException(500, detail="Forced failure to demonstrate ACID rollback")
        return {"ok": True, "list_id": lst.id, "recipe_id": r.id}
