from django.urls import path
from rest_framework.routers import DefaultRouter
from .usuario.views import UsuarioView, login
from .turmas.views import TurmaView

router = DefaultRouter()
router.register(r'usuario', UsuarioView, basename='usuario')
router.register(r'turma', TurmaView, basename='turma')
urlpatterns = router.urls
urlpatterns.append(path('login/', login))
