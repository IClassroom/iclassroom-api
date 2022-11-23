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
        self.base_route = "/api/matricula/"
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
        Teste para criação de uma matrícula
        """
        _, user, class_id = self.create_class_and_authenticate()
        token, user2 = self.authenticate(self.test_user2)
        self.test_matricula['turma_id'] = class_id
        self.test_matricula['usuario_id'] = user2['id']
        response = self.client.post(self.base_route, self.test_matricula, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_not_create_matricula_with_invalid_turma_id(self):
        """
        Teste para criação de uma matrícula com id da turma invalido
        """
        _, user, class_id = self.create_class_and_authenticate()
        token, user2 = self.authenticate(self.test_user2)
        self.test_matricula['turma_id'] = 200
        self.test_matricula['usuario_id'] = user2['id']
        response = self.client.post(self.base_route, self.test_matricula, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_should_not_create_matricula_with_invalid_usuario_id(self):
        """
        Teste para criação de uma matrícula com id da turma invalido
        """
        _, user, class_id = self.create_class_and_authenticate()
        token, user2 = self.authenticate(self.test_user2)
        self.test_matricula['turma_id'] = class_id
        self.test_matricula['usuario_id'] = 57
        response = self.client.post(self.base_route, self.test_matricula, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_matriculas(self):
        """
        Teste para listagem de todas as matrículas
        """
        _, user, class_id = self.create_class_and_authenticate()
        token, user2 = self.authenticate(self.test_user2)
        self.test_matricula['turma_id'] = class_id
        self.test_matricula['usuario_id'] = user2['id']
        self.client.post(self.base_route, self.test_matricula, HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(self.base_route, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_matricula_by_id(self):
        """
        Teste para listagem de uma matrícula específica
        """
        _, user, class_id = self.create_class_and_authenticate()
        token, user2 = self.authenticate(self.test_user2)
        self.test_matricula['turma_id'] = class_id
        self.test_matricula['usuario_id'] = user2['id']
        response = self.client.post(self.base_route, self.test_matricula, HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(f"{self.base_route}{response.data['id']}/", HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_matricula(self):
        """
        Teste para deleção de uma matricula
        """
        _, user, class_id = self.create_class_and_authenticate()
        token, user2 = self.authenticate(self.test_user2)
        self.test_matricula['turma_id'] = class_id
        self.test_matricula['usuario_id'] = user2['id']
        response = self.client.post(self.base_route, self.test_matricula, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete(f"{self.base_route}{response.data['id']}/", HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_not_get_matricula_with_invalid_id(self):
        """
        Teste para listagem de uma matrícula com id inválido
        """
        _, user, class_id = self.create_class_and_authenticate()
        token, user2 = self.authenticate(self.test_user2)
        self.test_matricula['turma_id'] = class_id
        self.test_matricula['usuario_id'] = user2['id']
        response = self.client.post(self.base_route, self.test_matricula, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(f"{self.base_route}100/", HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

