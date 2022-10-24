from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets

from api.models import Usuario
from api.serializers import UsuarioSerializer

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

# Create your views here.
class UsuarioView(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def perform_create(self, serializer):
        senha = make_password(self.request.data['password'])

        serializer.save(password=senha)

    def perform_update(self, serializer):
        senha = make_password(self.request.data['password'])

        serializer.save(password=senha)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get("email")
    senha = request.data.get("senha")
    
    if email is None or senha is None:
        return Response({'error': 'Email e senha necessários'},
                        status=HTTP_400_BAD_REQUEST)
    
    user = Usuario.objects.filter(email__iexact = email)[0]
    print(user.__str__)
    print(user.nome)
    print(type(user))

    if not user:
        return Response({'error': 'Usuário não encontrado'},
                        status=HTTP_404_NOT_FOUND)
    
    if user.check_password(senha):
        
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({'token': token.key},
                        status=HTTP_200_OK)
    else:
        return Response({'error': 'Credenciais inválidas'},
                        status=HTTP_404_NOT_FOUND)
    