from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import Turma
from .serializers import TurmaSerializer

import random
import string

class TurmaView(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer

    def perform_create(self, serializer):

        letters = ''.join(random.sample(string.ascii_uppercase, 4))
        digits = ''.join(random.sample(string.digits, 4))

        sample_list = list(letters + digits)
        sample_list = random.shuffle(sample_list)

        codigo = ''.join(sample_list)

        serializer.save(codigo=codigo)
