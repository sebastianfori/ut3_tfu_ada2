#!/usr/bin/env bash

BASE="http://localhost:8000"
API_KEY="supersecreta-UT5"

echo "Creando producto 1 si no existe..."
STATUS_PRODUCT=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/products/1")
if [ "$STATUS_PRODUCT" = "404" ]; then
  curl -s -X POST "$BASE/products/" \
    -H "Content-Type: application/json" \
    -H "x-api-key: $API_KEY" \
    -d '{"name":"Harina","unit":"g"}'
  echo
else
  echo "Producto 1 ya existe (status $STATUS_PRODUCT)"
fi
echo

echo "Creando receta 1 si no existe..."
STATUS_RECIPE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/recipes/1")
if [ "$STATUS_RECIPE" = "404" ]; then
  curl -s -X POST "$BASE/recipes/" \
    -H "Content-Type: application/json" \
    -H "x-api-key: $API_KEY" \
    -d '{"name":"Pancakes","instructions":"Mezclar y cocinar","items":[{"product_id":1,"quantity":200}]}'
  echo
else
  echo "Receta 1 ya existe (status $STATUS_RECIPE)"
fi
echo

echo "Creando nueva shopping list..."
LIST_RESPONSE=$(curl -s -X POST "$BASE/shopping-lists/" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d "{\"name\":\"Lista semanal $(date +%s)\"}")
echo "$LIST_RESPONSE"

# requiere jq para parsear JSON
LIST_ID=$(echo "$LIST_RESPONSE" | jq -r '.id // empty')
if [ -z "$LIST_ID" ]; then
  echo "No se pudo obtener LIST_ID, usando 1 por defecto"
  LIST_ID=1
fi
echo

echo "Agregando receta 1 a la lista $LIST_ID..."
curl -s -X POST "$BASE/recipes/1/add-to-list?list_id=$LIST_ID" \
  -H "x-api-key: $API_KEY"
echo
echo

SOAP_BODY=$(cat <<EOF
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetRecipeById>
      <id>1</id>
    </GetRecipeById>
  </soap:Body>
</soap:Envelope>
EOF
)

echo "Consultando receta 1 por SOAP..."
curl -s -X POST "$BASE/soap/" \
  -H "Content-Type: text/xml" \
  -d "$SOAP_BODY"
echo
echo
