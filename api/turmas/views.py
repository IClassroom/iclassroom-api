from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import Turma
from .serializers import TurmaSerializer, UsuarioTurmaSerializer

import random
import string

class TurmaView(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer

    def perform_create(self, serializer):
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        serializer.save(codigo=codigo)

    @action(detail=False, methods=['POST'])
    def matricula(self, request):
        serializer = UsuarioTurmaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
