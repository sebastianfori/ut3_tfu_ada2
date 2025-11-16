# api/app/routers/soap.py
from fastapi import APIRouter, Request, Response, HTTPException, Depends
from app.application.services import RecipeService
from app.routers.recipes import get_recipe_service  # reutilizamos el mismo service
import xml.etree.ElementTree as ET

router = APIRouter(prefix="/soap", tags=["soap"])

@router.post("/", response_class=Response)
async def soap_get_recipe_by_id(
    request: Request,
    svc: RecipeService = Depends(get_recipe_service),
):
    body_bytes = await request.body()

    try:
        root = ET.fromstring(body_bytes)
    except ET.ParseError:
        # XML inválido
        xml_resp = """
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
            <soap:Fault>
              <faultcode>Client</faultcode>
              <faultstring>Invalid XML</faultstring>
            </soap:Fault>
          </soap:Body>
        </soap:Envelope>
        """.strip()
        return Response(content=xml_resp, media_type="text/xml", status_code=400)

    # Buscamos cualquier tag <id> en el body, ignorando namespaces
    id_elem = root.find(".//id")
    if id_elem is None or not id_elem.text:
        xml_resp = """
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
            <soap:Fault>
              <faultcode>Client</faultcode>
              <faultstring>Missing id</faultstring>
            </soap:Fault>
          </soap:Body>
        </soap:Envelope>
        """.strip()
        return Response(content=xml_resp, media_type="text/xml", status_code=400)

    try:
        rid = int(id_elem.text)
    except ValueError:
        xml_resp = """
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
            <soap:Fault>
              <faultcode>Client</faultcode>
              <faultstring>Invalid id</faultstring>
            </soap:Fault>
          </soap:Body>
        </soap:Envelope>
        """.strip()
        return Response(content=xml_resp, media_type="text/xml", status_code=400)

    # Lógica de negocio: usamos el RecipeService
    try:
        recipe = svc.get(rid)
    except LookupError:
        xml_resp = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
            <soap:Fault>
              <faultcode>Client</faultcode>
              <faultstring>Recipe {rid} not found</faultstring>
            </soap:Fault>
          </soap:Body>
        </soap:Envelope>
        """.strip()
        return Response(content=xml_resp, media_type="text/xml", status_code=404)

    # Armamos la respuesta SOAP con la receta
    xml_resp = f"""
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <GetRecipeByIdResponse>
          <id>{recipe.id}</id>
          <name>{recipe.name}</name>
          <instructions>{recipe.instructions}</instructions>
        </GetRecipeByIdResponse>
      </soap:Body>
    </soap:Envelope>
    """.strip()

    return Response(content=xml_resp, media_type="text/xml")
