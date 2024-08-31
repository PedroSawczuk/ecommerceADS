from django.urls import path
from .views import *


urlpatterns = [
    path('cadastro/', UsuarioCreateView.as_view(), name='cadusuario'),
    path('usuarios/perfil/', PerfilUsuarioView.as_view(), name='perfil_user'),
]