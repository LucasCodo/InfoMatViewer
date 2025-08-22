import json
from functools import reduce
from time import time as timestamp

import peewee
from peewee import *

from app.configs import DB_SETTINGS, APPSETTINGS
from app.enumerations import PermissionsType
from datetime import datetime, timedelta

database = PostgresqlDatabase(**DB_SETTINGS)
FORMATTING_DATE = "%d-%m-%Y"


class BaseModel(Model):
    time_stamp = IntegerField(default=int(timestamp()), null=True)

    class Meta:
        database = database


class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


class Users(BaseModel):
    email = TextField(unique=True)
    disable = BooleanField(default=False)


class InfoMat(BaseModel):
    title = TextField()
    author = JSONField()
    publication_year = TextField()
    cover_image = TextField()  # capa
    abstract = TextField()  # resumo
    matters = JSONField()  # assuntos
    sub_matters = JSONField(null=True)
    availability = TextField(null=True)
    address = TextField(null=True)
    summary = TextField(null=True)
    tags = JSONField()  # tags
    number_of_pages = TextField()
    isbn = TextField()
    issn = TextField()
    typer = TextField()  # Tipo de material
    language = TextField(default="PT-BR")
    publisher = TextField()  # Editora
    volume = IntegerField()
    series = TextField()
    edition = TextField()
    reprint_update = TextField()
    number_of_hits = IntegerField(default=0)


class Review(BaseModel):
    book = ForeignKeyField(InfoMat, backref='reviews')
    user = ForeignKeyField(Users, backref='reviews')
    rating = FloatField()


class InfoMatList(BaseModel):
    name = TextField()
    user = ForeignKeyField(Users, backref='infoMatLists')
    observable = BooleanField(default=False)


class InfoMatListItems(BaseModel):
    infoMat = ForeignKeyField(InfoMat, backref='listInfoMatsbook')
    id_list = ForeignKeyField(InfoMatList, backref="listInfoMats")


class Permissions(BaseModel):
    user = ForeignKeyField(Users, backref="UserPermissions")
    expiration_date = DateTimeField(
        default=datetime.now, null=True)  # caso o valor seja nulo, a permissão não expira
    permission_type = TextField()
    disabled = BooleanField(default=False, null=True)


database.create_tables([Users, InfoMat, InfoMatList, InfoMatListItems, Review, Permissions])


def register_permission(_user: Users, permission_type: str,
                        expiration_date: datetime | None = datetime.now()+timedelta(days=7),
                        disabled: bool = False
                        ) -> Permissions:
    permission = Permissions(user=_user, permission_type=permission_type,
                             expiration_date=expiration_date, disabled=disabled)
    permission.save()
    return permission


def revoke_permission(permission: Permissions) -> None:
    permission.disabled = False
    permission.save()


def get_permissions(_user: Users) -> list[Permissions]:
    permissions = Permissions.select().where(
        (_user.id == Permissions.user) &
        (
                (Permissions.expiration_date > datetime.now()) |
                (Permissions.expiration_date in [None])
        ) &
        (Permissions.disabled == False)
    )
    return permissions


# Função para adicionar ou atualizar um review
def add_or_update_review(book_id, user_id, rating):
    review, created = Review.get_or_create(book=book_id, user=user_id, defaults={'rating': rating})
    if created:
        return review
    else:
        review.rating = rating
        review.save()
        return review


# Função para pegar uma Review de um usuario especifico
def read_review(book_id, user_id):
    try:
        _review = Review.get(Review.book == book_id and Review.user == user_id)
        return _review
    except Review.DoesNotExist:
        return None


# Função para pegar a média de avaliação de um livro
def get_avg_review(book_id):
    # Calcula a média do rating para um livro específico
    average_rating = (
        Review
        .select(fn.AVG(Review.rating).alias('avg_rating'))
        .where(Review.book == book_id)
        .scalar()  # Para obter o valor médio como um número em vez de um objeto
    )
    return average_rating


def delete_review(book_id, user_id) -> bool:
    try:
        _review = Review.get(Review.book == book_id and Review.user == user_id)
        _review.delete_instance()
        return True
    except Review.DoesNotExist:
        return False


# CRUD Users begin
# Função para criar um novo usuário
def create_user(email, disable=False) -> Users:
    _user, created = Users.get_or_create(email=email,
                                         defaults={
                                             "disable": disable}
                                         )
    return _user


def get_or_create_user(email, disable=False) -> tuple[Users, bool]:
    return Users.get_or_create(email=email,
                               defaults={
                                   "disable": disable}
                               )


# Função para ler um usuário pelo email
def read_user(email):
    try:
        _user = Users.get(Users.email == email)
        return _user
    except Users.DoesNotExist:
        return None


# Função para atualizar as informações de um usuário
def update_user(email, disable=None, permissions=None):
    _user = read_user(email)
    if _user:
        if disable is not None:
            _user.disable = disable
        if permissions is not None:
            _user.permissions = permissions
        _user.save()
        return _user
    else:
        return None


# Função para excluir um usuário pelo ID
def delete_user(user_id):
    _user = read_user(user_id)
    if _user:
        _user.delete_instance()
        return True
    else:
        return False


# CRUD Users end


# CRUD InfoMat begin
# Função para criar um novo registro InfoMat
def create_info_mat(title, author, publication_year, cover_image, abstract, matters,
                    sub_matters, availability, address, summary, tags,
                    number_of_pages, isbn, issn, typer, publisher, volume,
                    series, edition, reprint_update, language="PT-BR"):
    _info_mat = InfoMat.create(
        title=title,
        author=author,
        publication_year=publication_year,
        cover_image=cover_image,
        abstract=abstract,
        matters=matters,
        sub_matters=sub_matters,
        availability=availability,
        address=address,
        summary=summary,
        tags=tags,
        number_of_pages=number_of_pages,
        isbn=isbn,
        issn=issn,
        typer=typer,
        language=language,
        publisher=publisher,
        volume=volume,
        series=series,
        edition=edition,
        reprint_update=reprint_update
    )
    return _info_mat


def add_hit_in_info_mat(info_mat_id):
    try:
        _info_mat: InfoMat = InfoMat.get(InfoMat.id == info_mat_id)
        _info_mat.number_of_hits += 1
        _info_mat.save()
    except InfoMat.DoesNotExist:
        return None


def get_most_accessed_info_mats(limit=10):
    _info_mats = InfoMat.select().limit(limit).order_by(InfoMat.number_of_hits.desc())
    return list(_info_mats)


def get_all_info_mat():
    _info_mats = InfoMat.select()
    return list(_info_mats)


# Função para ler um registro InfoMat pelo ID
def read_info_mat(info_mat_id):
    try:
        _info_mat = InfoMat.get(InfoMat.id == info_mat_id)
        return _info_mat
    except InfoMat.DoesNotExist:
        return None


def read_info_mat_basic(info_mat_id):
    try:
        _info_mat: InfoMat = InfoMat.get(InfoMat.id == info_mat_id)
        _rating = get_avg_review(_info_mat.id)
        if _rating:
            _info_mat.rating = _rating
        else:
            _info_mat.rating = 0
        return _info_mat
    except InfoMat.DoesNotExist:
        return None


def read_top_rated_info_mat(limit: int = 10, min_reviews: int = 0) -> list[InfoMat]:
    """
    Retorna os materiais com melhor avaliação média.
    - limit: quantos itens retornar
    - min_reviews: mínimo de reviews exigidas (0 inclui materiais sem review com média=0;
    1 inclui apenas quem tem review)
    """
    avg_rating = fn.COALESCE(fn.AVG(Review.rating), 0).alias("rating")
    reviews_count = fn.COUNT(Review.id)

    query = (
        InfoMat
        .select(InfoMat, avg_rating, reviews_count.alias('reviews_count'))
        .join(Review, JOIN.LEFT_OUTER)                 # LEFT OUTER para incluir sem reviews (média=0)
        .group_by(InfoMat.id)
        .having(reviews_count >= min_reviews)          # filtra por mínimo de reviews, se quiser
        .order_by(avg_rating.desc(),                   # 1º: maior média
                  reviews_count.desc(),                # 2º: mais reviews
                  InfoMat.number_of_hits.desc())       # 3º: mais acessos (critério extra opcional)
        .limit(limit)
    )
    # Obs: cada item retornado carrega os campos extras avg_rating e reviews_count acessíveis
    # como atributos
    return list(query)


# Função para ler um registro InfoMat que corresponda a um valor em qualquer campo
def search_info_mat(string):
    try:
        _info_mat = InfoMat.select().where(
            (fn.CONCAT(
                InfoMat.title,
                InfoMat.author.cast('text'),
                InfoMat.publication_year,
                InfoMat.cover_image,
                InfoMat.abstract,
                InfoMat.matters.cast('text'),
                InfoMat.sub_matters.cast('text'),
                InfoMat.tags.cast('text'),
                InfoMat.number_of_pages,
                InfoMat.isbn,
                InfoMat.issn,
                InfoMat.typer,
                InfoMat.language,
                InfoMat.publisher,
                InfoMat.volume.cast('text'),
                InfoMat.series,
                InfoMat.edition,
                InfoMat.reprint_update
            ).contains(string))
        )
        return _info_mat
    except InfoMat.DoesNotExist:
        return None


# Função para atualizar informações de um registro InfoMat
def update_info_mat(info_mat_id, **kwargs):
    _info_mat = read_info_mat(info_mat_id)
    if _info_mat:
        for field, value in kwargs.items():
            setattr(_info_mat, field, value)
        _info_mat.save()
        return _info_mat
    else:
        return None


# Função para excluir um registro InfoMat pelo ID
def delete_info_mat(info_mat_id):
    _info_mat = read_info_mat(info_mat_id)
    if _info_mat:
        _info_mat.delete_instance()
        return True
    else:
        return False


# CRUD InfoMat end


# CRUD begin
# Função para criar uma nova lista de InfoMat
def create_info_mat_list(name, user_id, observable=False):
    _info_mat_list = InfoMatList.create(name=name, user=user_id, observable=observable)
    return _info_mat_list


# Função para ler uma lista de InfoMat pelo ID
def read_info_mat_list(_id):
    try:
        _info_mat_list = InfoMatList.get(InfoMatList.id == _id)
        return _info_mat_list
    except InfoMatList.DoesNotExist:
        return None


# Função para pegar os items de uma lista de materiais informacionais
def get_info_mat_list_items(list_id: int) -> list[InfoMat]:
    _info_mat_list_items = (InfoMatListItems
                            .select()
                            .join(InfoMat)
                            .where(InfoMatListItems.id_list == list_id))
    return list(map(lambda x: x.infoMat, _info_mat_list_items))


# Função para pegar as listas de um usuario especifico e itens da mesma
def get_my_info_mat_lists(user_id):  # no futuro alterar para email
    try:
        _query = (InfoMatList.select().where(
            InfoMatList.user == user_id
        ))
        list_info_mat_list = []
        for _info_mat_list in _query:
            _info_mat_list.listInfoMats = get_info_mat_list_items(_info_mat_list.id)
            list_info_mat_list.append(_info_mat_list)
        return list_info_mat_list
    except InfoMatList.DoesNotExist:
        return None


def is_my_info_mat_list(user_id: int, list_id: int) -> bool:
    return InfoMatList.select().where((InfoMatList.user == user_id) &
                                      (InfoMatList.id == list_id)).exists()


def info_mat_item_in_list(item_id: int,
                          list_id: int) -> bool:
    return InfoMatListItems.select().where(
        (InfoMatListItems.id_list == list_id) &
        (InfoMatListItems.infoMat == item_id)).exists()


# Função para atualizar informações de uma lista de InfoMat
def update_info_mat_list(info_mat_list_id, name=None, observable=None):
    _info_mat_list = read_info_mat_list(info_mat_list_id)
    if _info_mat_list:
        if name is not None:
            _info_mat_list.name = name
        if observable is not None:
            _info_mat_list.observable = observable
        _info_mat_list.save()
        return _info_mat_list
    else:
        return None


# Função para excluir uma lista de InfoMat pelo ID
def delete_info_mat_list(user_id, info_mat_list_id):
    _info_mat_list = InfoMatList.get(
        (InfoMatList.user == user_id) & (InfoMatList.id == info_mat_list_id))
    if _info_mat_list:
        InfoMatListItems.delete().where(InfoMatListItems.id_list == _info_mat_list.id).execute()
        _info_mat_list.delete_instance()
        return True
    else:
        return False


# Função para adicionar uma InfoMat a uma lista
def add_info_mat_item_to_list(info_mat_id, info_mat_list_id):
    try:
        list_info_mat = InfoMatListItems.create(infoMat=info_mat_id, id_list=info_mat_list_id)
        return list_info_mat
    except peewee.IntegrityError:
        return None


# Função para remover uma InfoMat de uma lista
def remove_info_mat_item_from_list(info_mat_id, info_mat_list_id):
    _query = InfoMatListItems.delete().where((InfoMatListItems.infoMat == info_mat_id) &
                                             (InfoMatListItems.id_list == info_mat_list_id))
    _query.execute()


def get_public_info_mat_list(info_mat_list_id: int):
    try:
        _info_mat_list = (InfoMatList
                          .select()
                          .where((InfoMatList.id == info_mat_list_id)
                                 & (InfoMatList.observable == True))
                          .get())
        _info_mat_list.listInfoMats = get_info_mat_list_items(info_mat_list_id)

        return _info_mat_list
    except InfoMatList.DoesNotExist:
        return None


def create_info_mat_list_and_add_items(_user_email, name: str, observable: bool,
                                       list_id_info_mat: list[int]):
    _user = read_user(_user_email)
    _info_mat_list = create_info_mat_list(name=name, user_id=_user, observable=observable)
    items = []
    for item in list_id_info_mat:
        element = add_info_mat_item_to_list(item, _info_mat_list)
        if element:
            items.append(element.infoMat)
    _info_mat_list.listInfoMats = items
    return _info_mat_list


# Boolean search
# Função para construir a query com base no JSON
def build_query(query_conditions):
    if 'and' in query_conditions:
        conditions = []
        for condition in query_conditions["and"]:
            for k, v in condition.items():
                conditions.append(build_query({k: v}))
        return reduce(lambda x, y: x & y, conditions)
    elif "or" in query_conditions:
        conditions = []
        for condition in query_conditions["or"]:
            for k, v in condition.items():
                conditions.append(build_query({k: v}))
        return reduce(lambda x, y: x | y, conditions)
    elif "not" in query_conditions:
        for k, v in query_conditions["not"].items():
            return reduce(lambda x:  x, [~fn.CONCAT(getattr(InfoMat, k)).contains(v)])
    else:
        k, v = [*tuple(*query_conditions.items())]
        return reduce(lambda x:  x, [fn.CONCAT(getattr(InfoMat, k)).contains(v)])


# Função que faz a busca da query gerada do json
def boolean_search(json_data):
    return InfoMat.select().where(build_query(json_data['query']))


new_user, admin_created = get_or_create_user(APPSETTINGS.admin_email)
if admin_created:
    register_permission(new_user, PermissionsType.FULL.name, expiration_date=None)


if __name__ == "__main__":
    # Exemplos de uso:

    # Criar um novo usuário
    new_user = create_user("user@example.com")
    print(new_user)
    # Ler um usuário pelo ID
    user = read_user(new_user.email)
    if user:
        print("Usuário encontrado:", user.email)
    else:
        print("Usuário não encontrado.")

    # Atualizar informações de um usuário
    update_user(email="user@example.com", disable=True)

    # Excluir um usuário pelo ID
    deleted = delete_user(new_user.id)
    if deleted:
        print("Usuário excluído com sucesso.")
    else:
        print("Usuário não encontrado.")
    # Exemplos de uso:

    # Criar um novo registro InfoMat
    new_info_mat = create_info_mat(
        title="Sample Book",
        author={"name": "John Doe", "affiliation": "Example University"},
        publication_year="2023",
        cover_image="cover_image_url",
        abstract="This is a sample book abstract.",
        matters=["Science", "Technology"],
        tags=["Sample", "Book"],
        number_of_pages="200",
        isbn="1234567890",
        issn="9876543210",
        typer="Book",
        publisher="Example Publishing",
        volume=1,
        series="Sample Series",
        edition="1st Edition",
        reprint_update="2023-09-20"
    )

    # Ler um registro InfoMat pelo ID
    info_mat = read_info_mat(new_info_mat.id)
    if info_mat:
        print("Registro InfoMat encontrado:", info_mat.title)
    else:
        print("Registro InfoMat não encontrado.")

    # Atualizar informações de um registro InfoMat
    update_info_mat(new_info_mat.id, title="Updated Sample Book Title")

    # Excluir um registro InfoMat pelo ID
    deleted = delete_info_mat(new_info_mat.id)
    if deleted:
        print("Registro InfoMat excluído com sucesso.")
    else:
        print("Registro InfoMat não encontrado.")
    # Exemplos de uso:

    # Criar uma nova lista de InfoMat
    new_info_mat_list = create_info_mat_list("My List", user)

    # Ler uma lista de InfoMat pelo ID
    info_mat_list = read_info_mat_list(new_info_mat_list.id)
    if info_mat_list:
        print("Lista de InfoMat encontrada:", info_mat_list.name)
    else:
        print("Lista de InfoMat não encontrada.")

    # Atualizar informações de uma lista de InfoMat
    update_info_mat_list(new_info_mat_list.id, name="Updated List Name")
    info_mat = create_info_mat(
        title="Sample Book",
        author=[{"name": "John Doe", "affiliation": "Example University"}],
        publication_year="2023",
        cover_image="cover_image_url",
        abstract="This is a sample book abstract.",
        matters=["Science", "Technology"],
        tags=["Sample", "Book"],
        number_of_pages="200",
        isbn="1234567890",
        issn="9876543210",
        typer="Book",
        publisher="Example Publishing",
        volume=1,
        series="Sample Series",
        edition="1st Edition",
        reprint_update="2023-09-20"
    )
    add_info_mat_item_to_list(info_mat, new_info_mat_list)

    # Remover uma InfoMat da lista
    remove_info_mat_item_from_list(info_mat, new_info_mat_list)

    # Excluir uma lista de InfoMat pelo ID
    deleted = delete_info_mat_list(user.id, new_info_mat_list.id)
    if deleted:
        print("Lista de InfoMat excluída com sucesso.")
    else:
        print("Lista de InfoMat não encontrada.")

    # Testando a função add_or_update_review
    def test_add_or_update_review():
        book_id = 2  # Substitua pelo ID do livro correto
        user_id = 2  # Substitua pelo ID do usuário correto
        rating = 3.8  # Substitua pela classificação desejada

        # Adicionar ou atualizar uma revisão
        review = add_or_update_review(book_id, user_id, rating)

        # Verificar se a revisão foi adicionada ou atualizada corretamente
        assert review.rating == rating


    test_add_or_update_review()

    # Testando a função read_review
    def test_read_review():
        book_id = 2  # Substitua pelo ID do livro correto
        user_id = 2  # Substitua pelo ID do usuário correto

        # Ler uma revisão
        review = read_review(book_id, user_id)

        # Verificar se a revisão foi lida corretamente
        assert review is not None


    test_read_review()

    # Testando a função get_avg_review
    def test_get_avg_review():
        book_id = 2  # Substitua pelo ID do livro correto

        # Obter a média da revisão
        avg_rating = get_avg_review(book_id)

        # Verificar se a média foi calculada corretamente
        print(f"A media de avaliação do livro {book_id} é", avg_rating)
        assert avg_rating is not None


    test_get_avg_review()

    # Testando a função delete_review
    def test_delete_review():
        book_id = 2  # Substitua pelo ID do livro correto
        user_id = 2  # Substitua pelo ID do usuário correto

        # Deletar uma revisão
        _result = delete_review(book_id, user_id)

        # Verificar se a revisão foi excluída corretamente
        assert _result is True


    test_delete_review()
