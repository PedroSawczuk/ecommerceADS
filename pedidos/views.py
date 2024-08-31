from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from carrinho.carrinho import Carrinho
from pedidos.forms import PedidoModelForm
from pedidos.models import ItemPedido, Pedido


class PedidoCreateView(LoginRequiredMixin, CreateView):
    form_class = PedidoModelForm
    success_url = reverse_lazy('resumopedido')
    template_name = 'pedido/formpedido.html'

    def form_valid(self, form):
        car = Carrinho(self.request)
        pedido = form.save(commit=False)
        usuario = self.request.user
        pedido.cliente = usuario
        pedido.save()
        for item in car:
            ItemPedido.objects.create(pedido=pedido,
                                      produto=item['produto'],
                                      preco=item['preco'],
                                      quantidade=item['quantidade'])
        car.limpar()
        self.request.session['idpedido'] = pedido.id
        return redirect('resumopedido')


class ResumoPedidoTemplateView(TemplateView):
    template_name = 'pedido/resumopedido.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pedido'] = Pedido.objects.get(id=self.request.session.get('idpedido'))
        return ctx

class ListaPedidosView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'pedido/lista_pedidos.html'  
    context_object_name = 'pedidos'

    def get_queryset(self):
        return Pedido.objects.filter(cliente=self.request.user)
    
class DetalhesPedidoView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'pedido/detalhes_pedido.html'
    context_object_name = 'pedido'

    def get_queryset(self):
        return Pedido.objects.filter(cliente=self.request.user)
    
class ExcluirPedidoView(LoginRequiredMixin, DeleteView):
    model = Pedido
    template_name = 'pedido/confirmar_exclusao.html'
    success_url = reverse_lazy('listar_pedidos')

    def get_queryset(self):
        return Pedido.objects.filter(cliente=self.request.user)

    def delete(self, request, *args, **kwargs):
        pedido = self.get_object()
        response = super().delete(request, *args, **kwargs)
        self.reajustar_indices()
        return response

    def reajustar_indices(self):
        pedidos = Pedido.objects.filter(cliente=self.request.user).order_by('criado')
        
        for i, pedido in enumerate(pedidos, start=1):
            pedido.indice = i
            pedido.save()
class PagarPedidoView(LoginRequiredMixin, UpdateView):
    model = Pedido
    fields = [] 
    template_name = 'pedido/confirmar_pagamento.html'

    def get_object(self, queryset=None):
        pedido = super().get_object(queryset)
        if pedido.cliente != self.request.user:
            raise PermissionDenied
        return pedido

    def form_valid(self, form):
        self.object.pago = True
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detalhes_pedido', kwargs={'pk': self.object.pk})