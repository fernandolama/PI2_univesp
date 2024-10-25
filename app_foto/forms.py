from django import forms
from django.forms import inlineformset_factory
from .models import Endereco, Telefone, Cliente, TamanhoFoto, PedidoImpressao, OrcamentoEvento, ItemPedido, RecursoEvento

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

    local_evento = forms.ModelChoiceField(queryset=Endereco.objects.all(), required=False, label="Local do Evento")
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

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'data_nascimento']  

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['cliente', 'rua', 'numero', 'complemento', 'bairro', 'cep', 'cidade', 'estado']

class TelefoneForm(forms.ModelForm):
    class Meta:
        model = Telefone
        fields = ['cliente', 'codigo_area', 'numero']

TelefoneFormSet = inlineformset_factory(Cliente, Telefone, fields=('codigo_area', 'numero'), extra=1, can_delete=True)
EnderecoFormSet = inlineformset_factory(Cliente, Endereco, fields=('rua', 'numero', 'complemento', 'bairro', 'cep', 'cidade', 'estado'), extra=1, can_delete=True)
RecursoEventoFormSet = inlineformset_factory(
    OrcamentoEvento,
    RecursoEvento,
    fields=('nome', 'preco'),
    extra=1,
    can_delete=True,
)