from django.test import TestCase, RequestFactory
from rest_framework import status
from django import setup
import os, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iclassroom_api.settings')
setup()

class UsuarioTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.base_route = "/api/usuario/"
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

    def authenticate(self):
        """
        Função auxiliar para realizar autenticação do usuário nos testes

        Retorna:

        Token: Token do usuário
        Id: Id do usuário
        """
        user = self.client.post(self.base_route, self.test_user)

        response = self.client.post(self.login_route, self.login_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['token'], user.data

    def test_should_create_user(self):
        """
        Testa a criação de um usuário e verifica se o status code foi 201
        """
        response = self.client.post(self.base_route, self.test_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_should_get_all_users(self):
        """
        Testa a listagem de todos os usuários e verifica se o status code foi 200
        """
        token, user = self.authenticate()
        response = self.client.get(self.base_route, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_get_user_by_id(self):
        """
        Testa a listagem de um usuário específico e verifica se o status code foi 200
        """
        token, data = self.authenticate()
        response = self.client.get(f'{self.base_route}{data["id"]}/', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_update_user(self):
        """
        Testa a atualização de um usuário e verifica se o status code foi 200
        """
        token, data = self.authenticate()
        data["nome"] = "Teste 2"
        data["email"] = "teste2@gmail.com"
        data["password"] = self.test_user["password"]

        user = json.dumps(data)

        response = self.client.put(f'{self.base_route}{data["id"]}/', data=user, content_type='application/json',
                                    HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_update_specific_field(self):
        """
        Testa a atualização de um campo específico de um usuário e verifica se o status code foi 200
        """
        token, data = self.authenticate()
        data["nome"] = "Teste 2"
        data["password"] = self.test_user["password"]

        user = json.dumps(data)

        response = self.client.patch(f'{self.base_route}{data["id"]}/', data=user, content_type='application/json',
                                    HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_delete_user(self):
        """
        Testa a deleção de um usuário e verifica se o status code foi 204
        """
        token, data = self.authenticate()
        response = self.client.delete(f'{self.base_route}{data["id"]}/', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_return_404_when_user_not_found(self):
        """
        Testa a listagem de um usuário inexistente e verifica se o status code foi 404
        """
        token, user = self.authenticate()
        response = self.client.get(f'{self.base_route}0/', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
