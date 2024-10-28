from django.http import JsonResponse
from django.shortcuts import render, redirect,  get_object_or_404
from .forms import ItemPedidoForm, TamanhoFotoForm, PedidoImpressaoForm, RecursoEventoForm, OrcamentoEventoForm, ClienteForm, EnderecoForm, TelefoneFormSet, EnderecoFormSet, ItemPedidoFormSet
from .models import ItemPedido, TamanhoFoto, PedidoImpressao, RecursoEvento, OrcamentoEvento, Cliente

def homepage(request):
    return render(request, 'homepage.html')

# Create

def novo_tamanho_foto(request):
    if request.method == 'POST':
        form = TamanhoFotoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_tamanhos_foto')
    else:
        form = TamanhoFotoForm()
    return render(request, 'novo_tamanho_foto.html', {'form': form})

def novo_pedido(request):
    if request.method == 'POST':
        pedido_form = PedidoImpressaoForm(request.POST)
        item_formset = ItemPedidoFormSet(request.POST)

        if pedido_form.is_valid() and item_formset.is_valid():
            pedido = pedido_form.save()
            item_formset.instance = pedido
            item_formset.save()
            return redirect('listar_pedidos')

    else:
        pedido_form = PedidoImpressaoForm()
        item_formset = ItemPedidoFormSet()

    return render(request, 'novo_pedido.html', {
        'pedido_form': pedido_form,
        'item_formset': item_formset,
    })

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
            orcamento_form.save_m2m()  # Salva relações Many-to-Many, com os recursos adicionais

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

def listar_tamanhos_foto(request):
    tamanhos = TamanhoFoto.objects.all()
    return render(request, 'listar_tamanhos_foto.html', {'tamanhos': tamanhos})

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

def editar_tamanho_foto(request, pk):
    tamanho_foto = get_object_or_404(TamanhoFoto, pk=pk)
    
    if request.method == 'POST':
        form = TamanhoFotoForm(request.POST, instance=tamanho_foto)
        
        if form.is_valid():
            form.save()
            return redirect('listar_tamanhos_foto')
    
    else:
        form = TamanhoFotoForm(instance=tamanho_foto)

    return render(request, 'editar_tamanho_foto.html', {
        'form': form,
        'tamanho_foto': tamanho_foto,
    })

def editar_orcamento(request, pk):
    orcamento = get_object_or_404(OrcamentoEvento, pk=pk)
    
    if request.method == 'POST':
        orcamento_form = OrcamentoEventoForm(request.POST, instance=orcamento)
        endereco_form = EnderecoForm(request.POST) if 'Outro' in request.POST.get('local_evento', '') else None
        
        if orcamento_form.is_valid() and (not endereco_form or endereco_form.is_valid()):
            orcamento = orcamento_form.save(commit=False)

            if endereco_form:
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
        pedido_form = PedidoImpressaoForm(request.POST, instance=pedido)
        formset = ItemPedidoFormSet(request.POST, instance=pedido)
        
        if pedido_form.is_valid() and formset.is_valid():
            pedido_form.save()
            formset.save()
            return redirect('listar_pedidos')
    
    else:
        pedido_form = PedidoImpressaoForm(instance=pedido)
        formset = ItemPedidoFormSet(instance=pedido)

    return render(request, 'editar_pedido.html', {
        'pedido_form': pedido_form,
        'formset': formset
    })

# Delete

def excluir_tamanho_foto(request, pk):
    tamanho = get_object_or_404(TamanhoFoto, pk=pk)
    if request.method == 'POST':
        tamanho.delete()
        return redirect('listar_tamanhos_foto')
    return render(request, 'confirmar_exclusao.html', {'objeto': tamanho, 'tipo': 'Tamanho de foto'})

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