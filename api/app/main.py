from fastapi import FastAPI
from .db import Base, engine
from .routers import products, recipes, shopping_lists

# Crear tablas al inicio (simple para demo académica)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Libro de Recetas API", version="1.0")

@app.get("/")
def root():
    return {"status": "ok", "service": "recipes-api"}

app.include_router(products.router)
app.include_router(recipes.router)
app.include_router(shopping_lists.router)
