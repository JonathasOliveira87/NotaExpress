from django.contrib import admin
from .models import Produto, Movimentacao, categoriaProduto, LocalProduto

admin.site.register(Produto)
admin.site.register(Movimentacao)
admin.site.register(categoriaProduto)
admin.site.register(LocalProduto)