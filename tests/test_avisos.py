from django.test import TestCase, RequestFactory
from rest_framework import status
from django import setup
import os, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iclassroom_api.settings')
setup()

class AvisoTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.create_user_route = "/api/usuario/"
        self.create_class_route = "/api/turma/"
        self.base_route = "/api/aviso/"
        self.login_route = "/api/login/"

        self.test_user = {
            "nome": "Teste",
            "email": "teste@gmail.com",
            "password": "123456"
        }

        self.login_user = {
            "email": "teste@gmail.com",
            "password": "123456"
        }

        self.test_class = {
            "codigo": "123456",
            "titulo": "Teste",
            "descricao": "Teste"
        }

        self.test_notice = {
            "usuario_id": None,
            "turma_id": None,
            "titulo": "Titulo do aviso",
            "descricao": "Descrição do aviso",
        }

    def authenticate(self):
        """
        Função auxiliar para realizar autenticação do usuário nos testes

        Retorna:

        Token: Token do usuário
        Id: Id do usuário
        """
        user = self.client.post(self.create_user_route, self.test_user)

        response = self.client.post(self.login_route, self.login_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['token'], user.data

    def create_class_and_authenticate(self):
        """
        Função auxiliar para criar uma turma

        Retorna:

        Id: Id da turma
        """
        token, user = self.authenticate()
        response = self.client.post(self.create_class_route, self.test_class, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return token, user, response.data['id']

    def test_should_get_all_notices(self):
        """
        Teste para obter todos os avisos
        """
        token, user, class_id = self.create_class_and_authenticate()
        response = self.client.get(self.base_route, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_notice(self):
        """
        Teste para criação de um aviso
        """
        token, user, class_id = self.create_class_and_authenticate()
        self.test_notice['turma_id'] = class_id
        self.test_notice['usuario_id'] = user['id']
        response = self.client.post(self.base_route, self.test_notice, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.data.usuario_id, status.HTTP_201_CREATED)
