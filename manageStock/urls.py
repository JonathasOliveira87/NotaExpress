from django.urls import path
from . import views

urlpatterns = [
    path('cadastrarProduto/', views.create, name='cadProduto'),
    path('verEstoque/', views.listar_produtos, name='verEstoque'),
    path('verProduto/<int:id>/', views.detalhes_produto, name='verProduto'),
    path('infoProduto/', views.ver_produto, name='infoProduto'),
    path('editarProduto/<int:id>/', views.update, name='editarProduto'),
]