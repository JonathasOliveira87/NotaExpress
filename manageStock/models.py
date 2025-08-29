from django.db import models

class categoriaProduto(models.Model):
    categoria = models.CharField(max_length=255)

    def __str__(self):
        return self.categoria
    
    class Meta:
        verbose_name = 'Gerenciar Categoria'


class LocalProduto(models.Model):
    local = models.CharField(max_length=255)

    def __str__(self):
        return self.local
    
    class Meta:
        verbose_name = 'Gerenciar Local'


class Produto(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    nome_fornecedor = models.CharField(max_length=100, default=None)
    categoria_produto = models.ForeignKey(categoriaProduto, on_delete=models.CASCADE, default=None)
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    foto_produto = models.ImageField(upload_to='produtos/', blank=True, null=True)
    local_produto = models.ForeignKey(LocalProduto, on_delete=models.CASCADE, default=None, blank=True, null=True)



    def __str__(self):
        return f"{self.codigo}\t{self.nome}\t{self.nome_fornecedor}\t{self.preco}\t{self.categoria_produto}"
    
    class Meta:
        verbose_name = 'Cadastrar Produto'

class Movimentacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=[('entrada', 'Entrada'), ('saida', 'Saída')])
    data = models.DateTimeField(auto_now_add=True)
