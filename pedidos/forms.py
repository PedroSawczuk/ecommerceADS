from django import forms

from pedidos.models import Pedido


class PedidoModelForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = []
