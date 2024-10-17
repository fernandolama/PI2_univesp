from django.shortcuts import render, redirect,  get_object_or_404
from .forms import PedidoImpressaoForm, OrcamentoEventoForm, PedidoForm, ClienteForm, ServicoForm
from .models import OrcamentoEvento, Cliente, Servico

def homepage(request):
    return render(request, 'homepage.html')

def novo_pedido_impressao(request):
    if request.method == 'POST':
        form = PedidoImpressaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = PedidoImpressaoForm()
    return render(request, 'novo_pedido_impressao.html', {'form': form})

def novo_orcamento_evento(request):
    if request.method == 'POST':
        form = OrcamentoEventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = OrcamentoEventoForm()
    return render(request, 'novo_orcamento_evento.html', {'form': form})

def novo_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o pedido no banco de dados
            return redirect('homepage')
    else:
        form = PedidoForm()
    return render(request, 'novo_pedido.html', {'form': form})

def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o cliente com os novos dados
            return redirect('homepage')
    else:
        form = ClienteForm()
    return render(request, 'cadastrar_cliente.html', {'form': form})

def listar_orcamentos(request):
    orcamentos = OrcamentoEvento.objects.all()
    return render(request, 'listar_orcamentos.html', {'orcamentos': orcamentos})

# View para editar orçamento
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

# View para criar um novo orçamento de evento
def novo_orcamento(request):
    if request.method == 'POST':
        form = OrcamentoEventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_orcamentos')
    else:
        form = OrcamentoEventoForm()
    return render(request, 'novo_orcamento.html', {'form': form})

# View para listar clientes
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'listar_clientes.html', {'clientes': clientes})

# View para editar cliente
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

# View para listar serviços
def listar_servicos(request):
    servicos = Servico.objects.all()
    return render(request, 'listar_servicos.html', {'servicos': servicos})

# View para editar serviço
def editar_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            return redirect('listar_servicos')
    else:
        form = ServicoForm(instance=servico)
    return render(request, 'editar_servico.html', {'form': form, 'servico': servico})

def novo_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_servicos')
    else:
        form = ServicoForm()
    return render(request, 'novo_servico.html', {'form': form})

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

def excluir_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        servico.delete()
        return redirect('listar_servicos')
    return render(request, 'confirmar_exclusao.html', {'objeto': servico, 'tipo': 'Serviço'})