from fastapi import APIRouter, HTTPException, Depends
from app.application.dtos import RecipeCreateDTO, RecipeDTO
from app.application.services import RecipeService
from app.infrastructure.unit_of_work import UnitOfWork
from app.infrastructure.sqlalchemy_repositories import SQLARecipeRepository, SQLAProductRepository, SQLAShoppingListRepository
from app.security import require_api_key  
router = APIRouter(prefix="/recipes", tags=["recipes"])

def get_recipe_service():
    uow = UnitOfWork()
    repo_factory = lambda session: SQLARecipeRepository(session)
    prod_repo_factory = lambda session: SQLAProductRepository(session)
    svc = RecipeService(uow, repo_factory, prod_repo_factory)
    svc.set_shopping_repo_factory(lambda session: SQLAShoppingListRepository(session))
    return svc

@router.get("/", response_model=list[RecipeDTO])
def list_recipes(svc: RecipeService = Depends(get_recipe_service)):
    return svc.list()

@router.get("/{rid}", response_model=RecipeDTO)
def get_recipe(rid: int, svc: RecipeService = Depends(get_recipe_service)):
    try:
        return svc.get(rid)
    except LookupError:
        raise HTTPException(404, detail="Not found")

@router.post("/", response_model=RecipeDTO, dependencies=[Depends(require_api_key)])
def create_recipe(payload: RecipeCreateDTO, svc: RecipeService = Depends(get_recipe_service)):
    try:
        return svc.create(payload)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
