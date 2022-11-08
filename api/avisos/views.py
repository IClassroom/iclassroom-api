from rest_framework import viewsets

from api.models import Aviso
from .serializers import AvisoSerializer

class AvisoView(viewsets.ModelViewSet):
    queryset = Aviso.objects.all()
    serializer_class = AvisoSerializer
