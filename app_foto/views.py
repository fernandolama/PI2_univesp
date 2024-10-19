from django.shortcuts import render, redirect,  get_object_or_404
from .forms import PedidoImpressaoForm, OrcamentoEventoForm, ClienteForm
from .models import PedidoImpressao, OrcamentoEvento, Cliente

def homepage(request):
    return render(request, 'homepage.html')

# Create

def novo_pedido(request):
    if request.method == 'POST':
        form = PedidoImpressaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pedidos')
    else:
        form = PedidoImpressaoForm()
    return render(request, 'novo_pedido.html', {'form': form})

def novo_orcamento(request):
    if request.method == 'POST':
        form = OrcamentoEventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_orcamentos')
    else:
        form = OrcamentoEventoForm()
    return render(request, 'novo_orcamento.html', {'form': form})

def novo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'cadastrar_cliente.html', {'form': form})

# Read

def listar_orcamentos(request):
    orcamentos = OrcamentoEvento.objects.all()
    return render(request, 'listar_orcamentos.html', {'orcamentos': orcamentos})

def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'listar_clientes.html', {'clientes': clientes})

def listar_pedidos(request):
    pedidos = PedidoImpressao.objects.all()
    return render(request, 'listar_pedidos.html', {'pedidos': pedidos})

# Update

def editar_orcamento(request, pk):
    orcamento = get_object_or_404(OrcamentoEvento, pk=pk)
    if request.method == 'POST':
        form = OrcamentoEventoForm(request.POST, instance=orcamento)
        if form.is_valid():
            form.save()
            return redirect('listar_orcamentos')
    else:
        form = OrcamentoEventoForm(instance=orcamento)
    return render(request, 'editar_orcamento.html', {'form': form, 'orcamento': orcamento})

def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'editar_cliente.html', {'form': form, 'cliente': cliente})

def editar_pedido(request, pk):
    pedido = get_object_or_404(PedidoImpressao, pk=pk)
    if request.method == 'POST':
        form = PedidoImpressaoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('listar_pedidos')
    else:
        form = PedidoImpressaoForm(instance=pedido)
    return render(request, 'editar_pedido.html', {'form': form, 'cliente': pedido})

# Delete

def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return render(request, 'confirmar_exclusao.html', {'objeto': cliente, 'tipo': 'Cliente'})

def excluir_orcamento(request, pk):
    orcamento = get_object_or_404(OrcamentoEvento, pk=pk)
    if request.method == 'POST':
        orcamento.delete()
        return redirect('listar_orcamentos')
    return render(request, 'confirmar_exclusao.html', {'objeto': orcamento, 'tipo': 'Orçamento'})

def excluir_pedido(request, pk):
    pedido = get_object_or_404(PedidoImpressao, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        return redirect('listar_pedidos')
    return render(request, 'confirmar_exclusao.html', {'objeto': pedido, 'tipo': 'Pedido'})