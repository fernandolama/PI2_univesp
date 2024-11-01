from django import forms
from django.forms import inlineformset_factory
from .models import Endereco, Telefone, Cliente, TamanhoFoto, PedidoImpressao, OrcamentoEvento, ItemPedido, RecursoEvento, TipoEvento

class TamanhoFotoForm(forms.ModelForm):
    class Meta:
        model = TamanhoFoto
        fields = ['medidas', 'preco_unitario']
        widgets = {
            'medidas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 10x15'}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 1,50'}),
        }

class PedidoImpressaoForm(forms.ModelForm):
    class Meta:
        model = PedidoImpressao
        fields = ['cliente']

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['tamanho_foto', 'quantidade']
        widgets = {
            'tamanho_foto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'}),
        }

class RecursoEventoForm(forms.ModelForm):
    class Meta:
        model = RecursoEvento
        fields = ['nome', 'preco']

    nome = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do recurso personalizado'}),
        label="Nome",
        required=True
    )
    preco = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço do recurso personalizado'}),
        label="Preço",
        required=True
    )

class TipoEventoForm(forms.ModelForm):
    class Meta:
        model = TipoEvento
        fields = ['nome', 'preco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Casamento'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 3200'}),
        }

class OrcamentoEventoForm(forms.ModelForm):
    class Meta:
        model = OrcamentoEvento
        fields = ['cliente', 'tipo_evento', 'data_evento', 'hora_evento', 'local_evento', 'logradouro', 'numero', 'complemento', 'bairro', 'cep', 'cidade', 'estado', 'recursos_adicionais', 'outros_detalhes']
        widgets = {
            'data_evento': forms.DateInput(attrs={'type': 'date'}),
            'hora_evento': forms.TimeInput(attrs={'type': 'time'}),
            'local_evento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Igreja, Salão de Festas, etc.'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua, Avenida, etc.'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apartamento, etc.'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 9}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 2}),
        }

    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Cliente"
    )
    tipo_evento = forms.ModelChoiceField(
        queryset=TipoEvento.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tipo de Evento"
    )
    recursos_adicionais = forms.ModelMultipleChoiceField(
        queryset=RecursoEvento.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Recursos Personalizados"
    )
    outros_detalhes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False,
        label="Outros Detalhes"
    )

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['logradouro', 'numero', 'complemento', 'bairro', 'cep', 'cidade', 'estado']
        widgets = {
            'logradouro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua, Avenida, etc.'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apartamento, etc.'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 9}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 2}),
        }

class TelefoneForm(forms.ModelForm):
    class Meta:
        model = Telefone
        fields = ['codigo_area', 'numero']
        widgets = {
                'codigo_area': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'DDD'}),
                'numero': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            }

TelefoneFormSet = inlineformset_factory(Cliente, Telefone, fields=('codigo_area', 'numero'),  form=TelefoneForm, extra=1, can_delete=True)
EnderecoFormSet = inlineformset_factory(Cliente, Endereco, fields=('logradouro', 'numero', 'complemento', 'bairro', 'cep', 'cidade', 'estado'), form=EnderecoForm, extra=1, can_delete=False)
ItemPedidoFormSet = inlineformset_factory(
    PedidoImpressao, ItemPedido, form=ItemPedidoForm, extra=1, can_delete=True
)