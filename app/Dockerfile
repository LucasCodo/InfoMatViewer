FROM python:3.11
LABEL authors="luss1"

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /src

# Copie os arquivos do projeto para o contêiner
COPY . /src/app

#coloque seu email
ENV admin_email=#
#coloque o google client id da aplicação
ENV GOOGLE_CLIENT_ID=#

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r /src/app/requirements.txt

# Comando para rodar o script Python
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]