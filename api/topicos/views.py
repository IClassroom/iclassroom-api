from rest_framework import viewsets

from api.models import Topico
from .serializers import TopicoSerializer

class TopicoView(viewsets.ModelViewSet):
    queryset = Topico.objects.all()
    serializer_class = TopicoSerializer
