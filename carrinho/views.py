from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from carrinho.carrinho import Carrinho
from catproduto.models import Produto
from carrinho.forms import CarrinhoAddProdutoForm


class CarrinhoAddFormView(FormView):
    form_class = CarrinhoAddProdutoForm
    success_url = reverse_lazy('listallprod')

    def post(self, request, *args, **kwargs):
        self.produto = Produto.objects.get(id=kwargs['idprod'])
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        cd = form.cleaned_data
        carrinho = Carrinho(self.request)
        carrinho.addProduto(produto=self.produto, quantidade=cd['quant'],
                            alterarquant=cd['alterar'])
        return super().form_valid(form)

    def form_invalid(self, form):
        # return redirect('listallprod')
        return super().form_invalid(form)

class CarrinhoRemoveView(View):

    def post(self, request, *args, **kwargs):
        self.produto = Produto.objects.get(id=kwargs['idprod'])
        carrinho = Carrinho(request)
        carrinho.removerProduto(self.produto)
        return redirect('carrinhodetalhe')

class CarrinhoDetalheTemplateView(TemplateView):
    template_name = 'carrinho/detalhe.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        carrinho = Carrinho(self.request)
        for item in carrinho:
            item['alterar'] = CarrinhoAddFormView(initial={'quant':item['quantidade'],
                                                           'alterar': True})
        contexto['carrinho'] = carrinho
        return contexto

