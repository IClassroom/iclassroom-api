from rest_framework import serializers
from api.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'id',
            'nome',
            'email',
            # 'password'
        )
        # xtra_kwargs = {
        #     'password': {
        #         'write_only': True,
        #     },
        # }
