from fastapi import Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from google.auth.transport import requests
from google.oauth2 import id_token
from app.configs import APPSETTINGS


def verify_google_token(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
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

        # Retornar informações do usuário, se necessário
        return id_info
    except ValueError as e:
        raise HTTPException(status_code=401, detail="Token inválido")