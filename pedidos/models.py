from django.contrib.auth.models import User
from django.db import models
from catproduto.models import Produto

class Pedido(models.Model):
    cliente = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)
    pago = models.BooleanField(default=False)
    indice = models.IntegerField(default=0)  # Adiciona o campo índice

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ('cliente', 'indice')  # Ordena por cliente e índice

    def __str__(self):
        return f'Pedido {self.id}'

    def get_total(self):
        return sum(item.get_custo() for item in self.itens_pedido.all())
    
    def get_total_formatado(self):
        return f"R$ {self.get_total():,.2f}".replace('.', ',')

    def get_status(self):
        return 'Pago' if self.pago else 'Pendente'

    def save(self, *args, **kwargs):
        if self.pk is None:  # Se for um novo pedido
            max_indice = Pedido.objects.filter(cliente=self.cliente).aggregate(models.Max('indice'))['indice__max']
            self.indice = (max_indice or 0) + 1
        super().save(*args, **kwargs)

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens_pedido', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, related_name='itens_produto', on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Item Pedido'
        verbose_name_plural = 'Itens Pedido'

    def __str__(self):
        return f'Item {self.id}'

    def get_custo(self):
        return self.preco * self.quantidade

    def get_total(self):
        return sum(item.get_custo() for item in self.itens_pedido.all())
    
    def get_preco_formatado(self):
        return f"R$ {self.preco:,.2f}".replace('.', ',')

    def get_custo_formatado(self):
        return f"R$ {self.get_custo():,.2f}".replace('.', ',')