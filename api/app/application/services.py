from .dtos import *
from .mappers import *
from ..domain.repositories import ProductRepository, RecipeRepository, ShoppingListRepository
from ..infrastructure.unit_of_work import UnitOfWork
from .decorators import retry_on_db_errors
from .cache import cache_get, cache_set, cache_delete


# --------------------------------------------------------------------
# PRODUCT SERVICE
# --------------------------------------------------------------------
class ProductService:
    def __init__(self, uow: UnitOfWork, repo_factory):
        self.uow = uow
        self.repo_factory = repo_factory

    @retry_on_db_errors
    def create(self, dto: ProductCreateDTO) -> ProductDTO:
        with self.uow as u:
            repo: ProductRepository = self.repo_factory(u.session)
            if repo.exists_by_name(dto.name):
                raise ValueError("Product already exists")
            created = repo.add(product_from_create(dto))
            #  invalidación de cache
            cache_delete("products:list")
            return product_to_dto(created)

    @retry_on_db_errors
    def list(self) -> list[ProductDTO]:
        #  Cache-Aside: primero intento cache
        cached = cache_get("products:list")
        if cached:
            return [ProductDTO(**x) for x in cached]

        with self.uow as u:
            repo: ProductRepository = self.repo_factory(u.session)
            data = [product_to_dto(x) for x in repo.list()]
            cache_set("products:list", [x.model_dump() for x in data], ttl_seconds=60)
            return data

    @retry_on_db_errors
    def get(self, pid: int) -> ProductDTO:
        # Cache individual
        key = f"products:{pid}"
        cached = cache_get(key)
        if cached:
            return ProductDTO(**cached)

        with self.uow as u:
            repo: ProductRepository = self.repo_factory(u.session)
            e = repo.get(pid)
            if not e:
                raise LookupError("Not found")
            dto = product_to_dto(e)
            cache_set(key, dto.model_dump(), ttl_seconds=60)
            return dto

    @retry_on_db_errors
    def update(self, pid: int, dto: ProductCreateDTO) -> ProductDTO:
        with self.uow as u:
            repo: ProductRepository = self.repo_factory(u.session)
            e = repo.update(pid, product_from_create(dto))
            if not e:
                raise LookupError("Not found")
            #  invalidación de cache
            cache_delete("products:list")
            cache_delete(f"products:{pid}")
            return product_to_dto(e)

    @retry_on_db_errors
    def delete(self, pid: int) -> None:
        with self.uow as u:
            repo: ProductRepository = self.repo_factory(u.session)
            repo.delete(pid)
            #  invalidación
            cache_delete("products:list")
            cache_delete(f"products:{pid}")


# --------------------------------------------------------------------
# RECIPE SERVICE
# --------------------------------------------------------------------
class RecipeService:
    def __init__(self, uow: UnitOfWork, repo_factory, prod_repo_factory):
        self.uow = uow
        self.repo_factory = repo_factory
        self.prod_repo_factory = prod_repo_factory

    @retry_on_db_errors
    def create(self, dto: RecipeCreateDTO) -> RecipeDTO:
        with self.uow as u:
            prod_repo: ProductRepository = self.prod_repo_factory(u.session)
            for it in dto.items:
                if not prod_repo.get(it.product_id):
                    raise ValueError(f"Unknown product {it.product_id}")

            repo: RecipeRepository = self.repo_factory(u.session)
            created = repo.add(recipe_from_create(dto))

            #  invalidación
            cache_delete("recipes:list")
            cache_delete(f"recipes:{created.id}")
            return recipe_to_dto(created)

    @retry_on_db_errors
    def list(self) -> list[RecipeDTO]:
        cached = cache_get("recipes:list")
        if cached:
            return [RecipeDTO(**x) for x in cached]

        with self.uow as u:
            repo: RecipeRepository = self.repo_factory(u.session)
            data = [recipe_to_dto(r) for r in repo.list()]
            cache_set("recipes:list", [x.model_dump() for x in data], 60)
            return data

    @retry_on_db_errors
    def get(self, rid: int) -> RecipeDTO:
        key = f"recipes:{rid}"
        cached = cache_get(key)
        if cached:
            return RecipeDTO(**cached)

        with self.uow as u:
            repo: RecipeRepository = self.repo_factory(u.session)
            e = repo.get(rid)
            if not e:
                raise LookupError("Not found")
            dto = recipe_to_dto(e)
            cache_set(key, dto.model_dump(), ttl_seconds=60)
            return dto

    @retry_on_db_errors
    def add_recipe_to_list(self, rid: int, list_id: int, fail: bool = False):
        with self.uow as u:
            rrepo: RecipeRepository = self.repo_factory(u.session)
            srepo: ShoppingListRepository = self._shopping_repo(u)

            r = rrepo.get(rid)
            if not r:
                raise LookupError("Recipe not found")
            lst = srepo.get(list_id)
            if not lst:
                raise LookupError("List not found")

            for it in r.items:
                srepo.add_item(lst.id, it.product_id, it.quantity)

            if fail:
                raise RuntimeError("Forced failure to demonstrate ACID rollback")

            cache_delete("recipes:list")
            return {"ok": True, "list_id": list_id, "recipe_id": rid}

    def _shopping_repo(self, u):
        return self.shopping_repo_factory(u.session)

    def set_shopping_repo_factory(self, factory):
        self.shopping_repo_factory = factory


# --------------------------------------------------------------------
# SHOPPING LIST SERVICE
# --------------------------------------------------------------------
class ShoppingListService:
    def __init__(self, uow: UnitOfWork, repo_factory):
        self.uow = uow
        self.repo_factory = repo_factory

    @retry_on_db_errors
    def create(self, dto: ShoppingListCreateDTO) -> ShoppingListDTO:
        with self.uow as u:
            repo: ShoppingListRepository = self.repo_factory(u.session)
            created = repo.add(shopping_list_from_create(dto))
            cache_delete("shopping_lists:list")
            return shopping_list_to_dto(created)

    @retry_on_db_errors
    def list(self) -> list[ShoppingListDTO]:
        cached = cache_get("shopping_lists:list")
        if cached:
            return [ShoppingListDTO(**x) for x in cached]

        with self.uow as u:
            repo: ShoppingListRepository = self.repo_factory(u.session)
            data = [shopping_list_to_dto(r) for r in repo.list()]
            cache_set("shopping_lists:list", [x.model_dump() for x in data], 60)
            return data
