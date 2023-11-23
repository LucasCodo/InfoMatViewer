
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app import database
from app.response_models import *

router = APIRouter()


@router.get("/informational-material/{info_mat_id}", response_model=InfoMatBasic)
async def info_mat(info_mat_id: int):
    """Endpoint para retornar informações básicas de um material informativo com o ID fornecido.

    Args:
    - info_mat_id (int): O ID do material informacional a ser recuperado.

    Returns:
    - InfoMatBasic: As informações básicas do material informativo."""
    return database.read_info_mat_basic(info_mat_id)


@router.get("/informational-material/{info_mat_id}/details", response_model=InfoMat)
async def info_mat_details(info_mat_id: int):
    """Endpoint para retornar os detalhes completos de um material informativo com o ID fornecido.

    Args:
    - info_mat_id (int): O ID do material informativo para recuperar os detalhes.

    Returns:
    - InfoMat: Os detalhes completos do materiais informacionais."""
    return database.read_info_mat(info_mat_id)


@router.get("/informational-material/search/", response_model=list[InfoMat])
async def search_info_mat(value: str):
    """ Endpoint para realizar a busca de materiais informacionais de forma generica.

    Busca materiais informacionais que possuam em algum campo a string desejada.

    Args:
    - value (str): String a ser usado como na busca dos materiais informacionais.

    Returns:
    - list[InfoMat]: Uma lista de materiais informacionais que correspondem ao critério de busca."""
    return database.search_info_mat(value)


@router.get("/list-informational-material/{cod}", response_model=InfoMatList)
async def get_public_list_informational_material(cod: int):
    """
        Endpoint para recuperar uma lista pública de materiais informacionais com base em um código
         específico.

        Args:
        - cod (int): O código que identifica a lista de materiais informacionais a ser recuperada.

        Returns:
        - InfoMatList: A lista pública de materiais informacionais correspondente ao código
         fornecido.
    """
    return database.get_public_info_mat_list(cod)


@router.post("/informational-material/search/with-boolean-operators")
async def search_info_mat_with_boolean_expression(json_query: JsonQuery):
    """
    Endpoint para obter um lista de materias informacionais a partir de uma query com
    operações booleanas.

    :param json_query:
    ### Exemplos de uso:
        exemplo1 = {
        "query": {
            "and": [
                {
                    "title": "Livro sobre Política"
                },
                {
                    "or": [
                        {
                            "publication_year": "2023"
                        },
                        {
                            "and": [
                                {
                                    "matters": "politics"
                                },
                                {
                                    "not": {
                                        "tags": "sports"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }

        exemplo2 = {"query": {'and': [{'matters': 'politics'}, {'not': {'tags': 'sports'}}]}}

        exemplo3 = {"query": {'and': [{'matters': 'politics'}, {'tags': 'government'}]}}

        exemplo4 = {"query": {"matters": "politics"}}

    ### Exemplo invalido:
        exemplo_invalido1 = {"query": {"matters": "politics", 'tags': 'government'}}

    :type json_query: `JsonQuery`

    :return: `retorna uma lista de InfoMat`

    :rtype: `list[InfoMat]`
    """

    try:
        # Executando a consulta
        resultado = database.boolean_search(dict(json_query))
    except TypeError:
        return HTMLResponse(status_code=422)
    return list(resultado)
