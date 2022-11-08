from rest_framework import serializers
from api.models import Topico

class TopicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topico
        fields = "__all__"
        extra_kwargs = {
            'id': {
                'read_only': True,
            },

        }
