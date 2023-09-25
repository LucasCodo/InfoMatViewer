from peewee import *
from time import time as timestamp
from enumerations import Permissions
import json
from configs import AppSettings


db_settings = dict(AppSettings())
db_settings.pop("admin_email")
database = PostgresqlDatabase(**db_settings)
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
    permissions = JSONField(default={Permissions.VIEW_INFO_MAT})


class InfoMat(BaseModel):
    title = TextField()
    author = JSONField()
    publication_year = TextField()
    cover_image = TextField()  # capa
    abstract = TextField()  # resumo
    matters = JSONField()  # assuntos
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


class Review(BaseModel):
    book = ForeignKeyField(InfoMat, backref='reviews')
    user = ForeignKeyField(Users, backref='reviews')
    rating = FloatField()


class InfoMatList(BaseModel):
    name = TextField()
    user = ForeignKeyField(Users, backref='infoMatLists')
    public = BooleanField(default=False)


class InfoMatListItems(BaseModel):
    infoMat = ForeignKeyField(InfoMat, backref='listInforMats')
    id_list = ForeignKeyField(InfoMatList, backref="listInforMats")


database.create_tables([Users, InfoMat, InfoMatList, InfoMatListItems])


# CRUD Users begin
# Função para criar um novo usuário
def create_user(email, disable=False, permissions=None):
    if permissions is None:
        permissions = [Permissions.VIEW_INFO_MAT]
    _user = Users.create(email=email, disable=disable, permissions=permissions)
    return _user


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
def create_info_mat(title, author, publication_year, cover_image, abstract, matters, tags,
                    number_of_pages, isbn, issn, typer, publisher, volume,
                    series, edition, reprint_update, language="PT-BR"):
    _info_mat = InfoMat.create(
        title=title,
        author=author,
        publication_year=publication_year,
        cover_image=cover_image,
        abstract=abstract,
        matters=matters,
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


# Função para ler um registro InfoMat pelo ID
def read_info_mat(info_mat_id):
    try:
        _info_mat = InfoMat.get(InfoMat.id == info_mat_id)
        return _info_mat
    except InfoMat.DoesNotExist:
        return None


# Função para ler um registro InfoMat que corresponda a um valor em qualquer campo
def search_info_mat(query):
    try:
        _info_mat = InfoMat.get(
            (fn.CONCAT(
                InfoMat.title,
                InfoMat.author.cast('text'),
                InfoMat.publication_year,
                InfoMat.cover_image,
                InfoMat.abstract,
                InfoMat.matters.cast('text'),
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
            ).contains(query))
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
def create_info_mat_list(name, user_id, public=False):
    _info_mat_list = InfoMatList.create(name=name, user=user_id, public=public)
    return _info_mat_list


# Função para ler uma lista de InfoMat pelo ID
def read_info_mat_list(user_id):
    try:
        _info_mat_list = InfoMatList.get(InfoMatList.user == user_id)
        return _info_mat_list
    except InfoMatList.DoesNotExist:
        return None


# Função para atualizar informações de uma lista de InfoMat
def update_info_mat_list(info_mat_list_id, name=None, public=None):
    _info_mat_list = read_info_mat_list(info_mat_list_id)
    if _info_mat_list:
        if name is not None:
            _info_mat_list.name = name
        if public is not None:
            _info_mat_list.public = public
        _info_mat_list.save()
        return _info_mat_list
    else:
        return None


# Função para excluir uma lista de InfoMat pelo ID
def delete_info_mat_list(info_mat_list_id):
    _info_mat_list = read_info_mat_list(info_mat_list_id)
    if _info_mat_list:
        _info_mat_list.delete_instance()
        return True
    else:
        return False


# Função para adicionar uma InfoMat a uma lista
def add_info_mat_to_list(info_mat_id, info_mat_list_id):
    list_info_mat = InfoMatListItems.create(infoMat=info_mat_id, id_list=info_mat_list_id)
    return list_info_mat


# Função para remover uma InfoMat de uma lista
def remove_info_mat_from_list(info_mat_id, info_mat_list_id):
    query = InfoMatListItems.delete().where((InfoMatListItems.infoMat == info_mat_id) &
                                            (InfoMatListItems.id_list == info_mat_list_id))
    query.execute()


if __name__ == "__main__":
    # Exemplos de uso:

    # Criar um novo usuário
    new_user = create_user("user@example.com", permissions=["VIEW_INFO_MAT", "EDIT_INFO_MAT"])

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
    add_info_mat_to_list(info_mat, new_info_mat_list)

    # Remover uma InfoMat da lista
    remove_info_mat_from_list(info_mat, new_info_mat_list)

    # Excluir uma lista de InfoMat pelo ID
    deleted = delete_info_mat_list(new_info_mat_list.id)
    if deleted:
        print("Lista de InfoMat excluída com sucesso.")
    else:
        print("Lista de InfoMat não encontrada.")