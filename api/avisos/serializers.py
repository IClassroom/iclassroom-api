from rest_framework import serializers
from api.models import Aviso

class TopicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aviso
        fields = "__all__"
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
        }
