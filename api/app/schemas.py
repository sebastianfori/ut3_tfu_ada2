from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from typing import List, Optional

# Productos
class ProductCreate(BaseModel):
    name: str
    unit: str

class ProductOut(BaseModel):
    id: int
    name: str
    unit: str
    model_config = ConfigDict(from_attributes=True)

# Recetas
class RecipeItemIn(BaseModel):
    product_id: int
    quantity: float = Field(gt=0)

class RecipeCreate(BaseModel):
    name: str
    instructions: Optional[str] = ""
    items: List[RecipeItemIn] = []

class RecipeItemOut(BaseModel):
    product_id: int
    quantity: float
    model_config = ConfigDict(from_attributes=True)

class RecipeOut(BaseModel):
    id: int
    name: str
    instructions: str
    items: List[RecipeItemOut] = []
    model_config = ConfigDict(from_attributes=True)

# Listas de compras
class ShoppingListCreate(BaseModel):
    name: str

class ShoppingListItemIn(BaseModel):
    product_id: int
    quantity: float = Field(gt=0)

class ShoppingListOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
