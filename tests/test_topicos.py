from django.test import TestCase, RequestFactory
from rest_framework import status
from django import setup
import os, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iclassroom_api.settings')
setup()

class TopicosTesteCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.create_user_route = "/api/usuario/"
        self.create_class_route = "/api/turma/"
        self.base_route = "/api/topico/"
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
            "descricao": "Teste",
            "professor_id": None
        }

        self.test_topic = {
            "turma_id": None,
            "titulo": "Teste",
            "descricao": "Teste"
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

    def test_create_topic(self):
        """
        Teste para criação de um tópico
        """
        token, user, class_id = self.create_class_and_authenticate()
        self.test_topic['turma_id'] = class_id
        response = self.client.post(self.base_route, self.test_topic, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_topics(self):
        """
        Teste para listagem de todos os tópicos
        """
        token, user, class_id = self.create_class_and_authenticate()
        self.test_topic['turma_id'] = class_id
        self.client.post(self.base_route, self.test_topic, HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(self.base_route, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_topic_by_id(self):
        """
        Teste para listagem de um tópico específico
        """
        token, user, class_id = self.create_class_and_authenticate()
        self.test_topic['turma_id'] = class_id
        response = self.client.post(self.base_route, self.test_topic, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(f"{self.base_route}{response.data['id']}/", HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_topic(self):
        """
        Teste para atualização de um tópico
        """
        token, user, class_id = self.create_class_and_authenticate()
        self.test_topic['turma_id'] = class_id
        response = self.client.post(self.base_route, self.test_topic, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.test_topic['titulo'] = "Teste 2"
        self.test_topic['descricao'] = "Teste 2"

        topic = json.dumps(self.test_topic)

        response = self.client.put(f"{self.base_route}{response.data['id']}/", data = topic, HTTP_AUTHORIZATION='Token ' + token,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_update_specific_item_from_topic(self):
        """
        Teste para atualização de um item espeífico de tópico
        """
        token, user, class_id = self.create_class_and_authenticate()
        self.test_topic['turma_id'] = class_id
        response = self.client.post(self.base_route, self.test_topic, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.test_topic['titulo'] = "Teste 2"

        topic = json.dumps(self.test_topic)

        response = self.client.patch(f"{self.base_route}{response.data['id']}/", data = topic, HTTP_AUTHORIZATION='Token ' + token,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_topic(self):
        """
        Teste para deleção de um tópico
        """
        token, user, class_id = self.create_class_and_authenticate()
        self.test_topic['turma_id'] = class_id
        response = self.client.post(self.base_route, self.test_topic, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete(f"{self.base_route}{response.data['id']}/", HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_not_create_topic_with_invalid_class_id(self):
        """
        Teste para criação de um tópico com id de turma inválido
        """
        token, user, class_id = self.create_class_and_authenticate()
        self.test_topic['turma_id'] = 100
        response = self.client.post(self.base_route, self.test_topic, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_not_get_topic_with_invalid_id(self):
        """
        Teste para listagem de um tópico com id inválido
        """
        token, user, class_id = self.create_class_and_authenticate()
        self.test_topic['turma_id'] = class_id
        response = self.client.post(self.base_route, self.test_topic, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(f"{self.base_route}100/", HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_not_update_topic_with_invalid_id(self):
        """
        Teste para atualização de um tópico com id inválido
        """
        token, user, class_id = self.create_class_and_authenticate()
        self.test_topic['turma_id'] = class_id
        response = self.client.post(self.base_route, self.test_topic, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.test_topic['titulo'] = "Teste 2"
        self.test_topic['descricao'] = "Teste 2"

        topic = json.dumps(self.test_topic)

        response = self.client.put(f"{self.base_route}100/", data = topic, HTTP_AUTHORIZATION='Token ' + token,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

