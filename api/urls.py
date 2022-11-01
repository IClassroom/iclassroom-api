from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UsuarioView, login

router = DefaultRouter()
router.register('usuario', UsuarioView, basename='Usuario')
urlpatterns = router.urls
urlpatterns.append(path('login/', login))
