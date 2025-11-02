from typing import Iterable, Optional
from sqlalchemy.orm import selectinload
from ..domain.repositories import ProductRepository, RecipeRepository, ShoppingListRepository
from ..domain.entities import Product, Recipe, RecipeItem, ShoppingList
from .models import ProductORM, RecipeORM, RecipeItemORM, ShoppingListORM, ShoppingListItemORM

# --- Mappers simples (ORM <-> Dominio) --- #
def to_product_entity(row: ProductORM) -> Product:
    return Product(id=row.id, name=row.name, unit=row.unit)

def to_recipe_entity(row: RecipeORM) -> Recipe:
    items = [RecipeItem(product_id=it.product_id, quantity=it.quantity) for it in row.items]
    return Recipe(id=row.id, name=row.name, instructions=row.instructions, items=items)

def to_shoppinglist_entity(row: ShoppingListORM) -> ShoppingList:
    return ShoppingList(id=row.id, name=row.name)

class SQLAProductRepository(ProductRepository):
    def __init__(self, session): self.session = session

    def add(self, p: Product) -> Product:
        obj = ProductORM(name=p.name, unit=p.unit)
        self.session.add(obj); self.session.flush()
        return to_product_entity(obj)

    def get(self, pid: int) -> Optional[Product]:
        obj = self.session.get(ProductORM, pid)
        return to_product_entity(obj) if obj else None

    def list(self) -> Iterable[Product]:
        rows = self.session.query(ProductORM).order_by(ProductORM.id).all()
        return [to_product_entity(r) for r in rows]

    def update(self, pid: int, p: Product) -> Product:
        obj = self.session.get(ProductORM, pid)
        if not obj: return None
        obj.name, obj.unit = p.name, p.unit
        self.session.flush()
        return to_product_entity(obj)

    def delete(self, pid: int) -> None:
        obj = self.session.get(ProductORM, pid)
        if obj: self.session.delete(obj)

    def exists_by_name(self, name: str) -> bool:
        return self.session.query(ProductORM).filter_by(name=name).first() is not None

class SQLARecipeRepository(RecipeRepository):
    def __init__(self, session): self.session = session

    def add(self, r: Recipe) -> Recipe:
        obj = RecipeORM(name=r.name, instructions=r.instructions or "")
        self.session.add(obj); self.session.flush()
        for it in r.items:
            self.session.add(RecipeItemORM(recipe_id=obj.id, product_id=it.product_id, quantity=it.quantity))
        self.session.flush()
        obj = self.session.query(RecipeORM).options(selectinload(RecipeORM.items)).get(obj.id)
        return to_recipe_entity(obj)

    def get(self, rid: int) -> Optional[Recipe]:
        obj = self.session.query(RecipeORM).options(selectinload(RecipeORM.items)).get(rid)
        return to_recipe_entity(obj) if obj else None

    def list(self) -> Iterable[Recipe]:
        rows = self.session.query(RecipeORM).options(selectinload(RecipeORM.items)).order_by(RecipeORM.id).all()
        return [to_recipe_entity(r) for r in rows]

class SQLAShoppingListRepository(ShoppingListRepository):
    def __init__(self, session): self.session = session

    def add(self, s: ShoppingList) -> ShoppingList:
        obj = ShoppingListORM(name=s.name)
        self.session.add(obj); self.session.flush()
        return to_shoppinglist_entity(obj)

    def get(self, lid: int) -> Optional[ShoppingList]:
        obj = self.session.get(ShoppingListORM, lid)
        return to_shoppinglist_entity(obj) if obj else None

    def list(self) -> Iterable[ShoppingList]:
        rows = self.session.query(ShoppingListORM).order_by(ShoppingListORM.id).all()
        return [to_shoppinglist_entity(r) for r in rows]

    def add_item(self, lid: int, product_id: int, quantity: float) -> None:
        self.session.add(ShoppingListItemORM(list_id=lid, product_id=product_id, quantity=quantity))
