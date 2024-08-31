from django.urls import path
from .views import *

urlpatterns = [
    path('add/', PedidoCreateView.as_view(), name='addpedido'),
    path('resumo/', ResumoPedidoTemplateView.as_view(), name='resumopedido'),
    path('usuarios/pedidos/', ListaPedidosView.as_view(), name='listar_pedidos'),
    path('usuarios/pedidos/<int:pk>/', DetalhesPedidoView.as_view(), name='detalhes_pedido'),
    path('usuarios/pedidos/<int:pk>/excluir/', ExcluirPedidoView.as_view(), name='excluir_pedido'),
    path('usuarios/pedidos/<int:pk>/pagar/', PagarPedidoView.as_view(), name='pagar_pedido'),

]