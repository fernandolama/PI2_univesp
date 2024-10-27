from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.homepage, name='homepage'), 

    # CRUD de Itens do Pedido
    path('pedido/<int:pedido_id>/adicionar-item/', views.adicionar_item_pedido, name='adicionar_item_pedido'),
    path('pedido/<int:pedido_id>/', views.ver_pedido, name='ver_pedido'),
    path('pedido/<int:pedido_id>/item/<int:item_id>/editar/', views.editar_item_pedido, name='editar_item_pedido'),
    path('pedido/<int:pedido_id>/item/<int:item_id>/excluir/', views.excluir_item_pedido, name='excluir_item_pedido'),
    
    # CRUD de Tamanhos de Impressões
    path('tamanhos/novo/', views.novo_tamanho, name='novo_tamanho'),
    path('tamanhos/', views.listar_tamanhos, name='listar_tamanhos'),
    path('tamanhos/editar/<int:pk>/', views.editar_tamanho, name='editar_tamanho'),
    path('tamanhos/excluir/<int:pk>/', views.excluir_tamanho, name='excluir_tamanho'), 
    
    # CRUD de Pedidos
    path('pedidos/novo/', views.novo_pedido, name='novo_pedido'),
    path('pedidos/', views.listar_pedidos, name='listar_pedidos'),
    path('pedidos/editar/<int:pk>/', views.editar_pedido, name='editar_pedido'),
    path('pedidos/excluir/<int:pk>/', views.excluir_pedido, name='excluir_pedido'), 

    # CRUD de Recursos
    path('recursos/novo/', views.novo_recurso, name='novo_recurso'),
    path('recursos/', views.listar_recursos, name='listar_recursos'),
    path('recursos/editar/<int:pk>/', views.editar_recurso, name='editar_recurso'),
    path('recursos/excluir/<int:pk>/', views.excluir_recurso, name='excluir_recurso'), 

    # CRUD de Orçamentos
    path('buscar-endereco/<int:cliente_id>/', views.buscar_endereco, name='buscar_endereco'),
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
