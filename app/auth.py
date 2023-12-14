from cachetools import cached, TTLCache
from fastapi import Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from google.auth.transport import requests
from google.oauth2 import id_token

from app.configs import APPSETTINGS
from app.database import create_user, get_permissions
from app.response_models import User


@cached(TTLCache(maxsize=256, ttl=1800))
def verify_google_token(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))) -> User:
    try:
        # Verificar o token do Google
        id_info = id_token.verify_oauth2_token(token, requests.Request(),
                                               APPSETTINGS.GOOGLE_CLIENT_ID)

        # Verificar se o token é válido para a sua aplicação
        if id_info['aud'] != APPSETTINGS.GOOGLE_CLIENT_ID:
            raise HTTPException(status_code=401, detail="Token inválido")
        org = id_info.get("hd", None)
        if org not in ["ufma.br", "discente.ufma.br"]:
            raise HTTPException(status_code=401, detail="The user is not part of this organization")
        user = create_user(id_info['email'])
        if user.disable:
            raise HTTPException(status_code=401)

        # Retornar informações do usuário, se necessário
        id_info["permissions"] = list(get_permissions(user))
        id_info["id"] = user.id
        return id_info
    except ValueError as _e:
        raise HTTPException(status_code=401, detail="Token inválido")
