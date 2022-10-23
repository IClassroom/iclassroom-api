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

# Executando o projeto

    python3 manage.py runserver

