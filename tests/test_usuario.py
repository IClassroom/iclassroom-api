from django.test import TestCase, RequestFactory
from django import setup
from rest_framework import status
import os
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iclassroom_api.settings')
setup()

class UsuarioTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.test_user = {
            "nome": "Rodrigo Santos da Silva",
            "email": "rss3@ic.ufal.br",
            "password": "123456"
        }

        self.base_route = '/api/usuario/'

    def test_should_get_all_users(self):
        """Testa se o endpoint de listagem de usuarios retorna todos os usuarios"""
        response = self.client.get(self.base_route)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_create_test_user(self):
        """Testa se o endpoint de criação de curso cria e retorna o curso criado"""

        response = self.client.post(self.base_route, self.test_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_get_test_user_by_id(self):
        """Testa se o endpoint de listagem de cursos retorna o curso especificado"""

        response = self.client.post(self.base_route, self.test_user, format='json')
        response = self.client.get(f'{self.base_route}{response.data["id"]}/'.format(response.data['id']))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_update_user(self):
        """Testa se o endpoint de atualização de curso atualiza e retorna o curso atualizado"""

        response = self.client.post(self.base_route, self.test_user, format='json')

        self.test_user["carga_horaria"] = 200

        user = json.dumps(self.test_user)

        response = self.client.put(f'{self.base_route}{response.data["id"]}/', data=user, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_update_specific_field(self):
        """Testa se o endpoint de atualização de curso atualiza o campo específico e retorna o curso atualizado"""

        response = self.client.post(self.base_route, self.test_user)

        self.test_user["titulo"] = "Novo título"

        user = json.dumps(self.test_user)

        response = self.client.put(f'{self.base_route}{response.data["id"]}/', data=user, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_return_404_for_not_found_user(self):
        """Testa se o endpoint de atualização de curso retorna 404 para um curso não encontrado"""
        response = self.client.get(f'{self.base_route}1a/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_remove_user(self):
        """Testa se o endpoint de remoção de curso remove e retorna 204"""

        response = self.client.post(self.base_route, self.test_user, format='json')

        response = self.client.delete(f'{self.base_route}{response.data["id"]}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
