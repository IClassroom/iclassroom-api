from rest_framework import serializers
from api.models import Usuario, Turma

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


class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = (
            'id',
            'titulo',
            'codigo',
            'descricao',
        )
        extra_kwargs = {
            'codigo': {
                'required': False,
                'read_only': True,
            },
        }
