from rest_framework import serializers
from api.models import Atividade

class AtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atividade
        fields = "__all__"
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
        }
