from django.test import TestCase, RequestFactory
from rest_framework import status
from django import setup
import os, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iclassroom_api.settings')
setup()

class MatriculaTesteCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.create_user_route = "/api/usuario/"
        self.create_class_route = "/api/turma/"
        self.base_route = "/api/turma/matricula/"
        self.login_route = "/api/login/"

        self.test_user = {
            "nome": "Teste",
            "email": "teste@gmail.com",
            "password": "123456"
        }

        self.test_user2 = {
            "nome": "Teste 2",
            "email": "teste2@gmail.com",
            "password": "123456"
        }

        self.login_user = {
            "email": "teste@gmail.com",
            "password": "123456"
        }

        self.test_class = {
            "codigo": "123456",
            "titulo": "Teste",
            "descricao": "Teste",
        }

        self.test_matricula = {
            "turma_id": None,
            "usuario_id": None,
            "tipo": 1,
            "expulso": False
        }

    def authenticate(self, user_data):
        """
        Função auxiliar para realizar autenticação do usuário nos testes

        Retorna:

        Token: Token do usuário
        Id: Id do usuário
        """
        user = self.client.post(self.create_user_route, user_data)

        response = self.client.post(self.login_route, self.login_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['token'], user.data

    def create_class_and_authenticate(self):
        """
        Função auxiliar para criar uma turma

        Retorna:

        Id: Id da turma
        """
        token, user = self.authenticate(self.test_user)
        self.test_class['professor_id'] = user['id']
        response = self.client.post(self.create_class_route, self.test_class, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return token, user, response.data['id']

    def test_create_matricula(self):
        """
        Teste para criação de um tópico
        """
        _, user, class_id = self.create_class_and_authenticate()
        token, user2 = self.authenticate(self.test_user2)
        self.test_matricula['turma_id'] = class_id
        self.test_matricula['usuario_id'] = user2['id']
        response = self.client.post(self.base_route, self.test_matricula, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
