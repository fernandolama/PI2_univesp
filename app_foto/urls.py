from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.homepage, name='homepage'), 

    # CRUD de Pedidos
    path('pedidos/novo/', views.novo_pedido, name='novo_pedido'),
    path('pedidos/', views.listar_pedidos, name='listar_pedidos'),
    path('pedidos/editar/<int:pk>/', views.editar_pedido, name='editar_pedido'),
    path('pedidos/excluir/<int:pk>/', views.excluir_pedido, name='excluir_pedido'), 

    # CRUD de Orçamentos
    path('orcamentos/novo/', views.novo_orcamento, name='novo_orcamento'),
    path('orcamentos/', views.listar_orcamentos, name='listar_orcamentos'),
    path('orcamentos/editar/<int:pk>/', views.editar_orcamento, name='editar_orcamento'),
    path('orcamentos/excluir/<int:pk>/', views.excluir_orcamento, name='excluir_orcamento'), 

    # CRUD de Clientes
    path('clientes/novo/', views.novo_cliente, name='novo_cliente'),  
    path('clientes/', views.listar_clientes, name='listar_clientes'),  
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),  
    path('clientes/excluir/<int:pk>/', views.excluir_cliente, name='excluir_cliente'), 
]
