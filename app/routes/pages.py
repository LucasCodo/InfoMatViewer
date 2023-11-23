from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.configs import AppSettings

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    """
   Endpoint para a página inicial.

   Args:
   - request (Request): Objeto da requisição HTTP.

   Returns:
   - HTMLResponse: Retorna a resposta HTML da página inicial com base no template index.html.
   """
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "admin_email": AppSettings().admin_email})