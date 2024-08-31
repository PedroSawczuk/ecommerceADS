from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from carrinho.forms import CarrinhoAddProdutoForm
from catproduto.models import Categoria, Produto

class IndexView(TemplateView):
    template_name = 'index.html'

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'produtos/categorias.html'
    context_object_name = 'categorias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = Produto.objects.all()
        return context

class ProdutosListView(ListView):
    model = Produto
    template_name = 'produtos/categorias.html'
    context_object_name = 'produtos'
    queryset = Produto.disponiveis.all()

    def get_queryset(self): 
        qs = super().get_queryset()
        slugcat = self.kwargs['slugcat'] 
        if slugcat:
            cat = Categoria.objects.get(slug=slugcat)
            qs = qs.filter(categoria=cat)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slugcat = self.kwargs['slugcat']
        if slugcat:
            context['categoria'] = Categoria.objects.get(slug=slugcat)
            context['categorias'] = Categoria.objects.all()
        return context

class ProdutoDetailView(DetailView):
    model = Produto
    template_name = "produtos/detalheproduto.html"

    def get_context_data(self, **kwargs):
        cont = super().get_context_data(**kwargs)
        cont['categorias'] = Categoria.objects.all()
        formaddcar = CarrinhoAddProdutoForm()
        cont['formadd'] = formaddcar
        return cont