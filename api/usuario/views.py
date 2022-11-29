from django.contrib.auth.hashers import make_password
from rest_framework import viewsets

from api.models import Usuario
from .serializers import UsuarioSerializer

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class UsuarioView(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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
    password = request.data.get("password")

    if email is None or password is None:
        return Response({'error': 'Email e senha necessários'},
                        status=status.HTTP_400_BAD_REQUEST)

    user = Usuario.objects.filter(email__iexact = email)[0]

    if not user:
        return Response({'error': 'Usuário não encontrado'},
                        status=status.HTTP_404_NOT_FOUND)

    if user.check_password(password):

        token, _ = Token.objects.get_or_create(user=user)

        userSerialized = UsuarioSerializer(user)

        return Response({'token': token.key, 'usuario': userSerialized.data},
                        status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Credenciais inválidas'},
                        status=status.HTTP_401_UNAUTHORIZED)
