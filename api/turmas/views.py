from rest_framework import viewsets

from api.models import Turma
from .serializers import TurmaSerializer

import random
import string

class TurmaView(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer

    def perform_create(self, serializer):
        source = string.ascii_uppercase + string.digits
        codigo = ''.join(random.sample(source, 7))

        serializer.save(codigo=codigo)
