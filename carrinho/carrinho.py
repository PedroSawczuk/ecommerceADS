from decimal import Decimal

from django.conf import settings
from django.http import request

from catproduto.models import Produto


class Carrinho(object):

    def __init__(self, request):
        """
        Iniciliza o carrinho de compras
        """
        self.session = request.session
        carrinho = self.session.get(settings.CART_SESSION_ID)
        if not carrinho:
            # salva um carrinho vazio na sessão
            carrinho = self.session[settings.CART_SESSION_ID] = {}
        self.carrinho = carrinho

    def addProduto(self, produto, quantidade=1, alterarquant=False):
        """
        Adiciona um produto ao carrinho ou atualiza a quantidade de um
        determinado produto
        :param produto: O produto a ser adicionado ou alterado a quant
        :param quantidade: A quantidade de unidades do produto a ser adicionado
        :param alterarquant: Quando necessário alterar a quantidade do produto no carrinho
        :return: Sem retorno
        """
        idproduto = str(produto.id)
        if idproduto not in self.carrinho:
            self.carrinho[idproduto] = {'quantidade': 0, 'preco': str(produto.preco)}
        if alterarquant:
            self.carrinho[idproduto]['quantidade'] = quantidade
        else:
            self.carrinho[idproduto]['quantidade'] += quantidade
        self._salvar()

    def _salvar(self):
        self.session.modified = True

    def removerProduto(self, produto):
        """
        Remove um produto do carrinho
        :param produto: O produto a ser removido
        :return: sem retorno
        """
        idproduto = str(produto.id)
        if idproduto in self.carrinho:
            del self.carrinho[idproduto]
            self._salvar()


    def __iter__(self):
        """
        Itera sobre o carrinho e obtem os produtos do banco de dados
        :return: sem retorno
        """
        idsprodutos = self.carrinho.keys()
        produtos = Produto.objects.filter(id__in=idsprodutos)
        carrinho = self.carrinho.copy()
        for p in produtos:
            carrinho[str(p.id)]['produto'] = p
        for item in carrinho.values():
            item['preco'] = Decimal(item['preco'])
            item['preco_total'] = item['preco'] * item['quantidade']
            yield item

    def __len__(self):
        """
        Soma as quantidades de itens que o carrinho possui
        :return: A quantidade itens do carrinho
        """
        return sum(item['quantidade'] for item in self.carrinho.values())

    def get_preco_total(self):
        return sum(Decimal(item['preco']) * item['quantidade'] for item in self.carrinho.values())

    def limpar(self):
        del self.session[settings.CART_SESSION_ID]
        self._salvar()