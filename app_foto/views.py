from django.http import JsonResponse
from django.shortcuts import render, redirect,  get_object_or_404
from .forms import ItemPedidoForm, TamanhoFotoForm, PedidoImpressaoForm, RecursoEventoForm, OrcamentoEventoForm, ClienteForm, EnderecoForm, TelefoneFormSet, EnderecoFormSet
from .models import ItemPedido, TamanhoFoto, PedidoImpressao, RecursoEvento, OrcamentoEvento, Cliente

def homepage(request):
    return render(request, 'homepage.html')

# Create

def adicionar_item_pedido(request, pedido_id):
    pedido = get_object_or_404(PedidoImpressao, id=pedido_id)
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False)
            item_pedido.pedido = pedido
            item_pedido.save()
            return redirect('ver_pedido', pedido_id=pedido.id)
    else:
        form = ItemPedidoForm()
    return render(request, 'adicionar_item_pedido.html', {'form': form, 'pedido': pedido})

def novo_tamanho(request):
    if request.method == 'POST':
        form = TamanhoFotoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_tamanhos')
    else:
        form = TamanhoFotoForm()
    return render(request, 'novo_tamanho.html', {'form': form})

def novo_pedido(request):
    if request.method == 'POST':
        form = PedidoImpressaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pedidos')
    else:
        form = PedidoImpressaoForm()
    return render(request, 'novo_pedido.html', {'form': form})

def novo_recurso(request):
    if request.method == 'POST':
        form = RecursoEventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_recursos')
    else:
        form = RecursoEventoForm()
    return render(request, 'novo_recurso.html', {'form': form})

def buscar_endereco(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    endereco = cliente.endereco_set.all().values('id', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado')
    
    return JsonResponse(list(endereco), safe=False)

def novo_orcamento(request):
    if request.method == 'POST':
        orcamento_form = OrcamentoEventoForm(request.POST)
        endereco_form = EnderecoForm(request.POST) if 'Outro' in request.POST.get('local_evento', '') else None

        if orcamento_form.is_valid() and (not endereco_form or endereco_form.is_valid()):
            orcamento = orcamento_form.save(commit=False)
            
            if endereco_form:
                # Salva o novo endereço
                novo_endereco = endereco_form.save()
                orcamento.local_evento = novo_endereco
            
            orcamento.save()
            orcamento_form.save_m2m()  # Salva relações Many-to-Many, como recursos adicionais

            return redirect('listar_orcamentos')

    else:
        orcamento_form = OrcamentoEventoForm()
        endereco_form = EnderecoForm()

    return render(request, 'novo_orcamento.html', {
        'orcamento_form': orcamento_form,
        'endereco_form': endereco_form
    })

def novo_cliente(request):
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        telefone_formset = TelefoneFormSet(request.POST)
        endereco_formset = EnderecoFormSet(request.POST)
        
        if cliente_form.is_valid() and telefone_formset.is_valid() and endereco_formset.is_valid():
            cliente = cliente_form.save()
            telefone_formset.instance = cliente
            telefone_formset.save()
            endereco_formset.instance = cliente
            endereco_formset.save()
            return redirect('listar_clientes')
    
    else:
        cliente_form = ClienteForm()
        telefone_formset = TelefoneFormSet()
        endereco_formset = EnderecoFormSet()
    return render(request, 'novo_cliente.html', {
        'cliente_form': cliente_form,
        'telefone_formset': telefone_formset,
        'endereco_formset': endereco_formset
    })

# Read

def ver_pedido(request, pedido_id):
    pedido = get_object_or_404(PedidoImpressao, id=pedido_id)
    itens = pedido.itens.all()
    total = pedido.calcular_total_pedido()
    return render(request, 'ver_pedido.html', {'pedido': pedido, 'itens': itens, 'total': total})

def listar_tamanhos(request):
    tamanhos = TamanhoFoto.objects.all()
    return render(request, 'listar_tamanhos.html', {'tamanhos': tamanhos})

def listar_recursos(request):
    recursos = RecursoEvento.objects.all()
    return render(request, 'listar_recursos.html', {'recursos': recursos})

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

def editar_item_pedido(request, pedido_id, item_id):
    pedido = get_object_or_404(PedidoImpressao, id=pedido_id)
    item = get_object_or_404(ItemPedido, id=item_id, pedido=pedido)

    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('ver_pedido', pedido_id=pedido.id)
    else:
        form = ItemPedidoForm(instance=item)

    return render(request, 'editar_item_pedido.html', {'form': form, 'pedido': pedido, 'item': item})

def editar_tamanho(request, pk):
    tamanho = get_object_or_404(TamanhoFoto, pk=pk)
    if request.method == 'POST':
        form = TamanhoFotoForm(request.POST, instance=tamanho)
        if form.is_valid():
            form.save()
            return redirect('listar_tamanhos')
    else:
        form = OrcamentoEventoForm(instance=tamanho)
    return render(request, 'editar_tamanho.html', {'form': form, 'tamanho': tamanho})

def editar_orcamento(request, pk):
    orcamento = get_object_or_404(OrcamentoEvento, pk=pk)
    
    if request.method == 'POST':
        orcamento_form = OrcamentoEventoForm(request.POST, instance=orcamento)
        endereco_form = EnderecoForm(request.POST) if 'Outro' in request.POST.get('local_evento', '') else None
        
        if orcamento_form.is_valid() and (not endereco_form or endereco_form.is_valid()):
            orcamento = orcamento_form.save(commit=False)

            if endereco_form:
                # Salva o endereço
                novo_endereco = endereco_form.save()
                orcamento.local_evento = novo_endereco

            orcamento.save()
            orcamento_form.save_m2m()
            
            return redirect('listar_orcamentos')
    
    else:
        orcamento_form = OrcamentoEventoForm(instance=orcamento)
        endereco_form = EnderecoForm() if not orcamento or orcamento.local_evento is None else None
    
    return render(request, 'editar_orcamento.html', {
        'orcamento_form': orcamento_form,
        'endereco_form': endereco_form
    })

def editar_recurso(request, pk):
    recurso = get_object_or_404(RecursoEvento, pk=pk)
    if request.method == 'POST':
        form = RecursoEventoForm(request.POST, instance=recurso)
        if form.is_valid():
            form.save()
            return redirect('listar_recursos')
    else:
        form = RecursoEventoForm(instance=recurso)
    return render(request, 'editar_recurso.html', {'form': form})

def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST, instance=cliente)
        telefone_formset = TelefoneFormSet(request.POST, instance=cliente)
        endereco_formset = EnderecoFormSet(request.POST, instance=cliente)

        if cliente_form.is_valid() and telefone_formset.is_valid() and endereco_formset.is_valid():
            cliente_form.save()
            telefone_formset.save()
            endereco_formset.save()
            return redirect('listar_clientes')
    
    else:
        cliente_form = ClienteForm(instance=cliente)
        telefone_formset = TelefoneFormSet(instance=cliente)
        endereco_formset = EnderecoFormSet(instance=cliente)
    
    return render(request, 'editar_cliente.html', {
        'cliente_form': cliente_form,
        'telefone_formset': telefone_formset,
        'endereco_formset': endereco_formset
    })

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

def excluir_item_pedido(request, pedido_id, item_id):
    pedido = get_object_or_404(PedidoImpressao, id=pedido_id)
    item = get_object_or_404(ItemPedido, id=item_id, pedido=pedido)

    if request.method == 'POST':
        item.delete()
        return redirect('ver_pedido', pedido_id=pedido.id)
    return render(request, 'confirmar_exclusao.html', {'objeto': item, 'tipo': 'Item'})

def excluir_tamanho(request, pk):
    tamanho = get_object_or_404(TamanhoFoto, pk=pk)
    if request.method == 'POST':
        tamanho.delete()
        return redirect('listar_tamanhos')
    return render(request, 'confirmar_exclusao.html', {'objeto': tamanho, 'tipo': 'Tamanho'})

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

def excluir_recurso(request, pk):
    recurso = get_object_or_404(RecursoEvento, pk=pk)
    if request.method == 'POST':
        recurso.delete()
        return redirect('listar_recursos')
    return render(request, 'confirmar_exclusao.html', {'objeto': recurso, 'tipo': 'Recurso'})