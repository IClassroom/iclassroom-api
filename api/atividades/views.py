from rest_framework import viewsets

from api.models import Atividade
from .serializers import AtividadeSerializer

class AtividadeView(viewsets.ModelViewSet):
    queryset = Atividade.objects.all()
    serializer_class = AtividadeSerializer
