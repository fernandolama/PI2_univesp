from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddressFormSet, CellphoneFormSet, ClientForm, ServiceForm
from .models import Client, Service

def home(request):
    return render(request, 'home.html')

def client_create(request, pk=None):
    if pk:
        client = Client.objects.get(pk=pk)
    else:
        client = None
    
    if request.method == 'POST':
        client_form = ClientForm(request.POST, instance=client)
        cellphone_formset = CellphoneFormSet(request.POST, instance=client)
        address_formset = AddressFormSet(request.POST, instance=client)
        if client_form.is_valid() and cellphone_formset.is_valid() and address_formset.is_valid():
            client_form.save()
            cellphone_formset.instance = client
            cellphone_formset.save()
            address_formset.instance = client
            address_formset.save()
            return redirect('client_list')
    else:
        client_form = ClientForm(instance=client)
        cellphone_formset = CellphoneFormSet(instance=client)        
        address_formset = AddressFormSet(instance=client)
    return render(request, 'client_form.html', {
        'client_form': client_form,
        'cellphone_formset': cellphone_formset,
        'address_formset': address_formset,
    })

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})

def client_edit(request, pk):
    client = Client.objects.get(pk=pk)
    if request.method == 'POST':
        client_form = ClientForm(request.POST, instance=client)
        cellphone_formset = CellphoneFormSet(request.POST, instance=client)
        address_formset = AddressFormSet(request.POST, instance=client)
        if client_form.is_valid() and cellphone_formset.is_valid() and address_formset.is_valid():
            client_form.save()
            cellphone_formset.instance = client
            cellphone_formset.save()
            address_formset.instance = client
            address_formset.save()
            return redirect('client_list')
    else:
        client_form = ClientForm(instance=client)
        cellphone_formset = CellphoneFormSet(instance=client)        
        address_formset = AddressFormSet(instance=client)
    return render(request, 'client_form.html', {
        'client_form': client_form,
        'cellphone_formset': cellphone_formset,
        'address_formset': address_formset,
    })

def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'client_confirm_delete.html', {'client': client })

def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_list.html')
    else:
        form = ServiceForm()

    return render(request, 'service_create.html', {'form': form})

def service_list(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'servicos': services})

def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'service_form.html', {'form': form})

def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    return render(request, 'service_confirm_delete.html', {'service': service})