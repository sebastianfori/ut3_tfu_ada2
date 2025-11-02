from dataclasses import dataclass
from typing import List

@dataclass
class Product:
    id: int | None
    name: str
    unit: str

@dataclass
class RecipeItem:
    product_id: int
    quantity: float

@dataclass
class Recipe:
    id: int | None
    name: str
    instructions: str
    items: List[RecipeItem]

@dataclass
class ShoppingListItem:
    product_id: int
    quantity: float

@dataclass
class ShoppingList:
    id: int | None
    name: str
