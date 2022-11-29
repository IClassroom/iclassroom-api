from rest_framework import viewsets

from api.models import UsuarioTurma
from .serializers import UsuarioTurmaSerializer

class UsuarioTurmaView(viewsets.ModelViewSet):
    queryset = UsuarioTurma.objects.all()
    serializer_class = UsuarioTurmaSerializer
