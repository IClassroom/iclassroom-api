from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UsuarioView, login

router = DefaultRouter()
router.register(r'usuario', UsuarioView, basename='usuario')
urlpatterns = router.urls
urlpatterns.append(path('login/', login))
