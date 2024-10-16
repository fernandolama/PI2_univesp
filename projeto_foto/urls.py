from django.contrib import admin
from django.urls import path
from app_foto import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('novo-pedido-impressao/', views.novo_pedido_impressao, name='novo_pedido_impressao'),
    path('novo-orcamento-evento/', views.novo_orcamento_evento, name='novo_orcamento_evento'),
    path('cadastrar-cliente/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('orcamentos/', views.listar_orcamentos, name='listar_orcamentos'),
    path('orcamentos/novo/', views.novo_orcamento, name='novo_orcamento'),
    path('servicos/', views.listar_servicos, name='listar_servicos'),
    path('servicos/novo/', views.novo_servico, name='novo_servico'),
    path('servicos/editar/<int:pk>/', views.editar_servico, name='editar_servico'),
    path('clientes/excluir/<int:pk>/', views.excluir_cliente, name='excluir_cliente'),
    path('orcamentos/excluir/<int:pk>/', views.excluir_orcamento, name='excluir_orcamento'),
    path('servicos/excluir/<int:pk>/', views.excluir_servico, name='excluir_servico'),
]

urlpatterns += [
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
]

urlpatterns += [
    path('orcamentos/', views.listar_orcamentos, name='listar_orcamentos'),
    path('orcamentos/editar/<int:pk>/', views.editar_orcamento, name='editar_orcamento'),
]

urlpatterns += [
    path('servicos/', views.listar_servicos, name='listar_servicos'),
    path('servicos/editar/<int:pk>/', views.editar_servico, name='editar_servico'),
]

