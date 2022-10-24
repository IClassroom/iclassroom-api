from rest_framework import serializers
from api.models import Usuario
 
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'nome',
            'email',
            'password'
        )
        xtra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

    # def restore_object(self, attrs, instance=None):
    #     usuario = super(UsuarioSerializer, self).restore_object(attrs, instance)
    #     return usuario