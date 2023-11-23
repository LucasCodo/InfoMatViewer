from app.routes.admin import router as router_admin
from app.routes.pages import router as router_pages
from app.routes.search import router as router_search
from app.routes.user import router as router_user

# Lista de roteadores com suas respectivas tags e descrições
routers = [
    (router_pages, "Web Pages", "Endpoints relacionados a páginas web"),
    (router_admin, "Admin", "Endpoints administrativos"),
    (router_user, "User", "Endpoints relacionados a usuários"),
    (router_search, "Search", "Endpoints de pesquisa")
]
