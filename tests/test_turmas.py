from django.test import TestCase, RequestFactory
from rest_framework import status
from django import setup
import os, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iclassroom_api.settings')
setup()

class TurmasTesteCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.create_user_route = "/api/usuario/"
        self.base_route = "/api/turma/"
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
            "titulo": "Turma A",
            "descricao": "Descrição da turma A de teste",
            "professor_id": None
        }

    def authenticate(self):
        """
        Função auxiliar para realizar autenticação do usuário nos testes

        Retorna:

        Token: Token do usuário
        Id: Id do usuário
        """
        user = self.client.post(self.create_user_route, self.test_user)
        self.test_class['professor_id'] = user.data['id']
        response = self.client.post(self.login_route, self.login_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['token'], user.data


    def test_should_get_all_classes(self):
        """
        Testa a listagem de todas as turmas e verifica se o status code foi 200
        """
        token, user = self.authenticate()
        response = self.client.get(self.base_route, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_create_class(self):
        """
        Testa a criação de uma turma e verifica se o status code foi 201
        """
        token, user = self.authenticate()
        response = self.client.post(self.base_route, self.test_class, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_get_class_by_id(self):
        """
        Testa a listagem de uma turma específica e verifica se o status code foi 200
        """
        token, user = self.authenticate()
        response = self.client.post(self.base_route, self.test_class, HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(f'{self.base_route}{response.data["id"]}/', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_update_class(self):
        """
        Testa a atualização de uma turma e verifica se o status code foi 200
        """
        token, user = self.authenticate()
        user["codigo"] = "123456"
        user["titulo"] = "Turma B"
        user["descricao"] = "Descrição da turma B de teste"
        user["professor_id"] = user['id']

        user = json.dumps(user)

        response = self.client.post(self.base_route, self.test_class, HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.put(f'{self.base_route}{response.data["id"]}/', data=user, HTTP_AUTHORIZATION='Token ' + token,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_update_specific_field_from_class(self):
        """
        Testa a atualização de um campo específico de uma turma e verifica se o status code foi 200
        """
        token, user = self.authenticate()
        user["codigo"] = "123456"
        user = json.dumps(user)

        response = self.client.post(self.base_route, self.test_class, HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.patch(f'{self.base_route}{response.data["id"]}/', data=user, HTTP_AUTHORIZATION='Token ' + token,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_delete_class(self):
        """
        Testa a deleção de uma turma e verifica se o status code foi 204
        """
        token, user = self.authenticate()
        response = self.client.post(self.base_route, self.test_class, HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete(f'{self.base_route}{response.data["id"]}/', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_not_create_class_with_invalid_data(self):
        """
        Testa a criação de uma turma com dados inválidos e verifica se o status code foi 400
        """
        token, user = self.authenticate()
        response = self.client.post(self.base_route, {}, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_not_update_class_with_invalid_data(self):
        """
        Testa a atualização de uma turma com dados inválidos e verifica se o status code foi 400
        """
        token, user = self.authenticate()

        user = json.dumps({})

        response = self.client.post(self.base_route, self.test_class, HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.put(f'{self.base_route}{response.data["id"]}/', data=user, HTTP_AUTHORIZATION='Token ' + token,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_not_get_class_with_invalid_id(self):
        """
        Testa a listagem de uma classe inexistente e verifica se o status code foi 404
        """
        token, user = self.authenticate()
        response = self.client.get(f'{self.base_route}0/', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
