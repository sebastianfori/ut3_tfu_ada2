#!/usr/bin/env bash
set -euo pipefail
BASE="http://localhost:8080"

echo "== Forzar fallo para demostrar rollback =="
curl -sS -X POST "$BASE/recipes/1/add-to-list?list_id=1&fail=true"
echo

echo "== Verificar que NO se insertaron duplicados =="
curl -sS "$BASE/shopping-lists/"
echo

