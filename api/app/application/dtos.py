from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from typing import List, Optional

# Productos
class ProductCreateDTO(BaseModel):
    name: str
    unit: str

class ProductDTO(BaseModel):
    id: int
    name: str
    unit: str
    model_config = ConfigDict(from_attributes=True)

# Recetas
class RecipeItemInDTO(BaseModel):
    product_id: int
    quantity: float = Field(gt=0)

class RecipeCreateDTO(BaseModel):
    name: str
    instructions: Optional[str] = ""
    items: List[RecipeItemInDTO] = []

class RecipeItemDTO(BaseModel):
    product_id: int
    quantity: float

class RecipeDTO(BaseModel):
    id: int
    name: str
    instructions: str
    items: List[RecipeItemDTO] = []

# Listas de compras
class ShoppingListCreateDTO(BaseModel):
    name: str

class ShoppingListDTO(BaseModel):
    id: int
    name: str
