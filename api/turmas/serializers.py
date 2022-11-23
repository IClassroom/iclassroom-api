from rest_framework import serializers
from api.models import Turma

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = "__all__"
        extra_kwargs = {
            'codigo': {
                'required': False,
                'read_only': True,
            },
        }

