from django import forms
from django.forms import inlineformset_factory
from .models import Endereco, Telefone, Cliente, TamanhoFoto, PedidoImpressao, OrcamentoEvento, ItemPedido, RecursoEvento, TipoEvento

class TamanhoFotoForm(forms.ModelForm):
    class Meta:
        model = TamanhoFoto
        fields = ['medidas', 'preco_unitario']

    medidas = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 10x15'}),
        label="Medidas da Impressão",
        required=True
    )
    preco_unitario = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço Unitário'}),
        label="Preço Unitário",
        required=True
    )

class PedidoImpressaoForm(forms.ModelForm):
    class Meta:
        model = PedidoImpressao
        fields = ['cliente', 'tamanho_foto', 'quantidade']

    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tamanho_foto = forms.ModelChoiceField(
        queryset=TamanhoFoto.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Selecione o tamanho da foto"
    )
    quantidade = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'}),
        label="Quantidade"
    )

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['tamanho_foto', 'quantidade']
    
    tamanho_foto = forms.ModelChoiceField(
        queryset=TamanhoFoto.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tamanho da Foto"
    )
    quantidade = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'}),
        label="Quantidade"
    )

class RecursoEventoForm(forms.ModelForm):
    class Meta:
        model = RecursoEvento
        fields = ['nome', 'preco']

    nome = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do recurso adicional'}),
        label="Nome do Recurso Adicional",
        required=True
    )
    preco = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço do recurso adicional'}),
        label="Preço do Recurso Adicional",
        required=True
    )

class OrcamentoEventoForm(forms.ModelForm):
    class Meta:
        model = OrcamentoEvento
        fields = ['cliente', 'tipo_evento', 'data_evento', 'hora_evento', 'local_evento', 'recursos_adicionais' , 'outros_detalhes']

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
    local_evento = forms.ModelChoiceField(
        queryset=Endereco.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Local do Evento",
        empty_label="Escolha um endereço ou selecione 'Outro' para adicionar um novo "
    )
    recursos_adicionais = forms.ModelMultipleChoiceField(
        queryset=RecursoEvento.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Selecione os recursos adicionais para este orçamento"
    )
    outros_detalhes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona a opção "Outro" ao local_evento
        self.fields['local_evento'].choices = list(self.fields['local_evento'].choices) + [("Outro", "Outro")]

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
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 8}),
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