from sqlalchemy import Column, Integer, String, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from ..db import Base

class ProductORM(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False)
    unit = Column(String(32), nullable=False)

class RecipeORM(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False)
    instructions = Column(String(2000), default="")
    items = relationship("RecipeItemORM", cascade="all, delete-orphan", back_populates="recipe")

class RecipeItemORM(Base):
    __tablename__ = "recipe_items"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    recipe = relationship("RecipeORM", back_populates="items")
    __table_args__ = (UniqueConstraint('recipe_id', 'product_id', name='uq_recipe_product'),)

class ShoppingListORM(Base):
    __tablename__ = "shopping_lists"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    items = relationship("ShoppingListItemORM", cascade="all, delete-orphan", back_populates="list")

class ShoppingListItemORM(Base):
    __tablename__ = "shopping_list_items"
    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey("shopping_lists.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    list = relationship("ShoppingListORM", back_populates="items")
