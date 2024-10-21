from django import forms
from .models import PedidoImpressao, RecursoEvento, OrcamentoEvento, Cliente, Endereco, Telefone

class PedidoImpressaoForm(forms.ModelForm):
    class Meta:
        model = PedidoImpressao
        fields = ['cliente', 'tamanho_foto', 'quantidade', 'preco_unitario']

    tamanho_foto = forms.ChoiceField(
        choices=PedidoImpressao.TAMANHO_OPCOES,
        widget=forms.Select(attrs={'class': 'form-control'})
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
        fields = ['cliente', 'tipo_evento', 'data_evento', 'local_evento', 'recursos_adicionais' , 'outros_detalhes']

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
        fields = [ 'rua', 'numero', 'complemento', 'bairro', 'cep', 'cidade', 'estado']

class TelefoneForm(forms.ModelForm):
    class Meta:
        model = Telefone
        fields = ['cliente', 'codigo_area', 'numero']