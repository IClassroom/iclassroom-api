# IClassroom - API

# Instalação -  Linux

1 - Crie e ative o ambiente virtual com os seguintes comandos

    python3 -m venv venv/
    source venv/bin/activate

2 - Instale as dependências

    pip install -r requirements.txt

# Configurando variáveis de ambiente

1 - Crie um arquivo .env na raiz do projeto e adicione as seguintes variáveis com seus valores

    DATABASE_NAME=
    DATABASE_USER=
    DATABASE_PASSWORD=
    DATABASE_HOST=
    DATABASE_PORT=
    DEBUG=True
    ALLOWED_HOSTS=*,

# Executando migrações

1 - Caso faça alterações nos modelos do projeto, execute o comando abaixo para gerar as migrações

    python manage.py makemigrations

2 - Após gerar as migrações, execute o comando abaixo para executar as migrações no banco de dados

        python manage.py migrate

# Executando o projeto

    python3 manage.py runserver

    ou

    gunicorn --bind 0.0.0.0:8000 setup.wsgi

# Testes

Para executar os testes, basta rodar o comando:

    python manage.py test

# Docker

Para buildar e subir os containers, utilize os seguintes comandos:

    docker build -t iclassroom-api .
    docker run -p 8000:8000 iclassroom-api

    ou

    docker-compose up | para subir o projeto
    docker-compose up --build | para buildar e subir o projeto

    (obs: pode usar a flag -d, de detached, para usar o mesmo terminal)
