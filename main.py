from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

import database
from configs import AppSettings
from response_models import *

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
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


@app.get("/informational-material/{info_mat_id}", response_model=InfoMatBasic)
async def info_mat(info_mat_id: int):
    """Endpoint para retornar informações básicas de um material informativo com o ID fornecido.

    Args:
    - info_mat_id (int): O ID do material informacional a ser recuperado.

    Returns:
    - InfoMatBasic: As informações básicas do material informativo."""
    return database.read_info_mat_basic(info_mat_id)


@app.get("/informational-material/{info_mat_id}/details", response_model=InfoMat)
async def info_mat_details(info_mat_id: int):
    """Endpoint para retornar os detalhes completos de um material informativo com o ID fornecido.

    Args:
    - info_mat_id (int): O ID do material informativo para recuperar os detalhes.

    Returns:
    - InfoMat: Os detalhes completos do materiais informacionais."""
    return database.read_info_mat(info_mat_id)


@app.get("/search/informational-material/", response_model=list[InfoMat])
async def search_info_mat(value: str):
    """ Endpoint para realizar a busca de materiais informacionais de forma generica.

    Busca materiais informacionais que possuam em algum campo a string desejada.

    Args:
    - value (str): String a ser usado como na busca dos materiais informacionais.

    Returns:
    - list[InfoMat]: Uma lista de materiais informacionais que correspondem ao critério de busca."""
    return database.search_info_mat(value)


@app.get("/list-informational-material/{cod}", response_model=InfoMatList)
async def get_public_list_informational_material(cod: int):
    """
        Endpoint para recuperar uma lista pública de materiais informacionais com base em um código específico.

        Args:
        - cod (int): O código que identifica a lista de materiais informacionais a ser recuperada.

        Returns:
        - InfoMatList: A lista pública de materiais informacionais correspondente ao código fornecido.
    """
    return database.get_public_info_mat_list(cod)


@app.post("/informational-material/")
async def add_info_mat(new_info_mat: InfoMat):
    """
        Endpoint para adicionar um novo materiais informacional.

        Args:
        - new_info_mat (InfoMat): Novo materiais informacional a ser adicionado.

        Returns:
        - None: Retorna nada ou uma confirmação de sucesso, dependendo da implementação do método
        `create_info_mat` no objeto `database`.
    """
    return database.create_info_mat(**dict(new_info_mat))


@app.post("/list-informational-material", response_model=InfoMatList)
async def create_list_info_mat(user_email: EmailStr, list_info_mat: InfoMatListPost):
    """
        Endpoint para criar uma nova lista de materiais informativos.

        Args:
        - list_info_mat (InfoMatListPost): Representa os dados da nova lista de materiais informativos a ser criada.

        Returns:
        - InfoMatListPost: Retorna os dados da lista de materiais informativos criada.

        TO DO: implementar função que cria uma infomatlist com nenhum ou varios itens.
    """
    return database.create_info_mat_list_and_add_items(user_email, list_info_mat.name,
                                                       list_info_mat.public,
                                                       list_info_mat.listIDsInfoMats)


@app.get("/list-informational-material/user/{user_email}", response_model=list[InfoMatList])
async def get_my_lists(user_email: EmailStr):
    """
        Endpoint para obter as listas de materiais informativos de um usuário específico.

        Args:
        - user_email (EmailStr): O endereço de e-mail do usuário para recuperar suas listas de
         materiais informativos.

        Returns:
        - list[InfoMatList]: Uma lista de listas de materiais informativos associadas ao usuário.
    """
    return database.get_my_info_mat_lists(database.read_user(user_email))
