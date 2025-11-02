from fastapi import FastAPI
from .db import Base, engine
from .infrastructure import models  # registra tablas
from .routers import products, recipes, shopping_lists 

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Libro de Recetas API (UT4 Patterns)", version="2.0")

@app.get("/")
def root():
    return {"status": "ok", "service": "recipes-api", "version": "2.0"}

app.include_router(products.router)
app.include_router(recipes.router)
app.include_router(shopping_lists.router)
