from rest_framework import viewsets

from api.models import Turma
from .serializers import TurmaSerializer

import random
import string

class TurmaView(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer

    def perform_create(self, serializer):
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        serializer.save(codigo=codigo)
