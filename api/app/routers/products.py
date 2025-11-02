from fastapi import APIRouter, HTTPException, Depends
from app.application.dtos import ProductCreateDTO, ProductDTO
from app.application.services import ProductService
from app.infrastructure.unit_of_work import UnitOfWork
from app.infrastructure.sqlalchemy_repositories import SQLAProductRepository
from app.security import require_api_key  # Gatekeeper

router = APIRouter(prefix="/products", tags=["products"])

def get_product_service():
    uow = UnitOfWork()
    repo_factory = lambda session: SQLAProductRepository(session)
    return ProductService(uow, repo_factory)

@router.get("/", response_model=list[ProductDTO])
def list_products(svc: ProductService = Depends(get_product_service)):
    return svc.list()

@router.get("/{pid}", response_model=ProductDTO)
def get_product(pid: int, svc: ProductService = Depends(get_product_service)):
    try:
        return svc.get(pid)
    except LookupError:
        raise HTTPException(404, detail="Not found")

# API Key para operaciones de escritura
@router.post("/", response_model=ProductDTO, dependencies=[Depends(require_api_key)])
def create_product(payload: ProductCreateDTO, svc: ProductService = Depends(get_product_service)):
    try:
        return svc.create(payload)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@router.put("/{pid}", response_model=ProductDTO, dependencies=[Depends(require_api_key)])
def update_product(pid: int, payload: ProductCreateDTO, svc: ProductService = Depends(get_product_service)):
    try:
        return svc.update(pid, payload)
    except LookupError:
        raise HTTPException(404, detail="Not found")

@router.delete("/{pid}", dependencies=[Depends(require_api_key)])
def delete_product(pid: int, svc: ProductService = Depends(get_product_service)):
    svc.delete(pid)
    return {"ok": True}
