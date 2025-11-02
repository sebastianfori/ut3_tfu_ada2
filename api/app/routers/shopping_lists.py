from fastapi import APIRouter, HTTPException, Depends
from app.application.dtos import ShoppingListCreateDTO, ShoppingListDTO
from app.application.services import ShoppingListService
from app.infrastructure.unit_of_work import UnitOfWork
from app.infrastructure.sqlalchemy_repositories import SQLAShoppingListRepository
from app.security import require_api_key  # 🔐 Gatekeeper

router = APIRouter(prefix="/shopping-lists", tags=["shopping lists"])

def get_shopping_list_service():
    uow = UnitOfWork()
    repo_factory = lambda session: SQLAShoppingListRepository(session)
    return ShoppingListService(uow, repo_factory)

@router.get("/", response_model=list[ShoppingListDTO])
def list_shopping_lists(svc: ShoppingListService = Depends(get_shopping_list_service)):
    return svc.list()

# 🔒 API Key requerida
@router.post("/", response_model=ShoppingListDTO, dependencies=[Depends(require_api_key)])
def create_shopping_list(payload: ShoppingListCreateDTO, svc: ShoppingListService = Depends(get_shopping_list_service)):
    return svc.create(payload)
