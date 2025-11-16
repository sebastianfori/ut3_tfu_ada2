from ..domain.entities import Product, Recipe, RecipeItem, ShoppingList
from .dtos import (
    ProductDTO, ProductCreateDTO,
    RecipeDTO, RecipeCreateDTO, RecipeItemDTO,
    ShoppingListDTO, ShoppingListCreateDTO
)

def product_from_create(dto: ProductCreateDTO) -> Product:
    return Product(id=None, name=dto.name, unit=dto.unit)

def product_to_dto(e: Product) -> ProductDTO:
    return ProductDTO(id=e.id, name=e.name, unit=e.unit)

def recipe_from_create(dto: RecipeCreateDTO) -> Recipe:
    items = [RecipeItem(product_id=i.product_id, quantity=i.quantity) for i in dto.items]
    return Recipe(id=None, name=dto.name, instructions=dto.instructions or "", items=items)

def recipe_to_dto(e: Recipe) -> RecipeDTO:
    return RecipeDTO(
        id=e.id, name=e.name, instructions=e.instructions,
        items=[RecipeItemDTO(product_id=i.product_id, quantity=i.quantity) for i in e.items]
    )


def shopping_list_from_create(dto: ShoppingListCreateDTO) -> ShoppingList:
    return ShoppingList(id=None, name=dto.name)

def shopping_list_to_dto(e: ShoppingList) -> ShoppingListDTO:
    return ShoppingListDTO(id=e.id, name=e.name)

shoppinglist_from_create = shopping_list_from_create
shoppinglist_to_dto = shopping_list_to_dto
