from django.urls import path
from rest_framework.routers import DefaultRouter
from .usuario.views import UsuarioView, login
from .turmas.views import TurmaView
from .topicos.views import TopicoView
from .matricula.views import UsuarioTurmaView
from .avisos.views import AvisoView

router = DefaultRouter()
router.register(r'usuario', UsuarioView, basename='usuario')
router.register(r'turma', TurmaView, basename='turma')
router.register(r'matricula', UsuarioTurmaView, basename='matricula')
router.register(r'topico', TopicoView, basename='topico')
router.register(r'aviso', AvisoView, basename='aviso')
urlpatterns = router.urls
urlpatterns.append(path('login/', login))
