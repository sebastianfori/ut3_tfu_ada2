from fastapi import APIRouter, HTTPException
from ..db import get_session
from .. import models, schemas

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=schemas.ProductOut)
def create_product(payload: schemas.ProductCreate):
    with get_session() as db:
        if db.query(models.Product).filter_by(name=payload.name).first():
            raise HTTPException(400, detail="Product already exists")
        p = models.Product(name=payload.name, unit=payload.unit)
        db.add(p)
        db.flush()
        # ✅ Convertir a Pydantic ANTES de cerrar sesión
        return schemas.ProductOut.model_validate(p)

@router.get("/", response_model=list[schemas.ProductOut])
def list_products():
    with get_session() as db:
        items = db.query(models.Product).order_by(models.Product.id).all()
        return [schemas.ProductOut.model_validate(x) for x in items]

@router.get("/{pid}", response_model=schemas.ProductOut)
def get_product(pid: int):
    with get_session() as db:
        p = db.get(models.Product, pid)
        if not p:
            raise HTTPException(404, detail="Not found")
        return schemas.ProductOut.model_validate(p)

@router.put("/{pid}", response_model=schemas.ProductOut)
def update_product(pid: int, payload: schemas.ProductCreate):
    with get_session() as db:
        p = db.get(models.Product, pid)
        if not p:
            raise HTTPException(404, detail="Not found")
        p.name = payload.name
        p.unit = payload.unit
        db.flush()
        return schemas.ProductOut.model_validate(p)

@router.delete("/{pid}")
def delete_product(pid: int):
    with get_session() as db:
        p = db.get(models.Product, pid)
        if not p:
            raise HTTPException(404, detail="Not found")
        db.delete(p)
        return {"ok": True}
