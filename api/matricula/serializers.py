from rest_framework import serializers
from api.models import UsuarioTurma


class UsuarioTurmaSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsuarioTurma
        fields = "__all__"

