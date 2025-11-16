#!/usr/bin/env bash
set -euo pipefail
BASE="http://localhost:8000"

echo "== Crear productos =="
curl -sS -X POST "$BASE/products/" -H 'Content-Type: application/json' -d '{"name":"Harina","unit":"g"}'
echo
curl -sS -X POST "$BASE/products/" -H 'Content-Type: application/json' -d '{"name":"Leche","unit":"ml"}'
echo

echo "== Listar productos =="
curl -sS "$BASE/products/"
echo

echo "== Crear receta Panqueques =="
curl -sS -X POST "$BASE/recipes/" -H 'Content-Type: application/json' -d '{
  "name":"Panqueques",
  "instructions":"Mezclar y dorar",
  "items":[{"product_id":1,"quantity":200},{"product_id":2,"quantity":300}]
}'
echo

echo "== Crear lista semanal =="
curl -sS -X POST "$BASE/shopping-lists/" -H 'Content-Type: application/json' -d '{"name":"Semanal"}'
echo

echo "== Agregar receta a la lista (ACID ok) =="
curl -sS -X POST "$BASE/recipes/1/add-to-list?list_id=1"
echo

echo "== Ver listas =="
curl -sS "$BASE/shopping-lists/"
echo
