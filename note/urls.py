from django.urls import path, include
from . import views


urlpatterns = [
    path('criarNota/', views.criarNota, name='criarNota'),
    path('criarOrdem/', views.criarOrdem, name='criarOrdem'),
    path('listarNota/', views.listarNotas, name='listarNota'),
    path('listarOrdem/', views.listarOrdens, name='listarOrdem'),
    path('infoNota/<int:ver_nota>/', views.detalhesNota, name='infoNota'),
    path('infoOrdem/(?P<ver_ordem>[0-9a-fA-F]+)/$', views.detalhesOrdem, name='infoOrdem'),
    path('encerrar-ordem/', views.encerrar_ordem, name='encerrar_ordem'),
    path('finalizar-ordem/', views.finalizar_ordem, name='finalizar_ordem'),
    path('dashboard/', views.dashboard, name='dashboard'),
]