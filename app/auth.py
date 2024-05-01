from cachetools import cached, TTLCache
from fastapi import Depends, HTTPException
from app.database import create_user, get_permissions
from app.response_models import User
from fastapi.security import OAuth2AuthorizationCodeBearer
import requests


@cached(TTLCache(maxsize=256, ttl=1800))
def verify_google_token(token: str = Depends(OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="https://oauth2.googleapis.com/token",
    scopes={
        "email": "Access your email address",
        "profile": "Access your basic profile information",
        "openid": ""
    }
))) -> User:
    token_info_url = "https://www.googleapis.com/oauth2/v1/tokeninfo"

    # Parâmetros da solicitação para a API
    params = {'access_token': token}

    # Faz a solicitação para a API
    response = requests.get(token_info_url, params=params)
    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Se a resposta foi bem-sucedida, retorna os dados
        token_info = response.json()
        email: str = token_info.get("email", "")
        if not (email.endswith("ufma.br") or email.endswith("discente.ufma.br")):
            raise HTTPException(status_code=401,
                                detail="The user is not part of this organization")
        user = create_user(email)
        if user.disable:
            raise HTTPException(status_code=401)
            # Retornar informações do usuário, se necessário
        token_info["permissions"] = list(get_permissions(user))
        token_info["id"] = user.id
        return token_info
    else:
        raise HTTPException(status_code=response.status_code)
