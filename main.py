from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.routes import routers

pendent_invoices = {}
app = FastAPI()
app.mount("/app/static", StaticFiles(directory="app/static"), name="static")


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Manipulador para redirecionar qualquer endpoint desconhecido para /redoc
@app.middleware("http")
async def redirect_unknown_endpoints(request: Request, call_next):
    try:
        response = await call_next(request)
        if response.status_code == 404:  # Verifica se o endpoint não foi encontrado
            return RedirectResponse(url="/redoc", status_code=302)
        return response
    except HTTPException as e:
        if e.status_code == 404:
            return RedirectResponse(url="/redoc", status_code=302)
        raise


# Incluir cada roteador na aplicação principal
for router, tag_name, tag_description in routers:
    app.include_router(router, tags=[tag_name])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="InfoMatViewer API",
        version="0.1.0",
        description="API da Vitrine virtual da biblioteca setorial da UFMA de Pinheiro.",
        routes=app.routes,
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://pbs.twimg.com/profile_images/1656379573150584832/05OE5sVJ_400x400.jpg"
    }

    # Adicionando descrições para todas as tags
    openapi_schema["tags"] = [
        {"name": _tag_name,
         "description": _tag_description} for _, _tag_name, _tag_description in routers
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
