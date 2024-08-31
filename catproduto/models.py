from django.db import models

class ProdutosManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(disponivel=True)

class Categoria(models.Model):
    nome = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ('nome',)

    def __str__(self):
        return self.nome

class Produto (models.Model):
    objects = models.Manager()
    disponiveis = ProdutosManager()
    nome = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    imagem = models.ImageField(upload_to='produtos/%Y/%m/%d', blank=True)
    descricao = models.TextField(blank=True)
    disponivel = models.BooleanField(default=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('nome',)
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome

