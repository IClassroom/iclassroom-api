from django.urls import path
from rest_framework.routers import DefaultRouter
from .usuario.views import UsuarioView, login
from .turmas.views import TurmaView
from .topicos.views import TopicoView
from .avisos.views import AvisoView
from .atividades.views import AtividadeView

router = DefaultRouter()
router.register(r'usuario', UsuarioView, basename='usuario')
router.register(r'turma', TurmaView, basename='turma')
router.register(r'topico', TopicoView, basename='topico')
router.register(r'aviso', AvisoView, basename='aviso')
router.register(r'atividade', AtividadeView, basename='atividade')
urlpatterns = router.urls
urlpatterns.append(path('login/', login))
