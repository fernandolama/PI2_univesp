from django import forms
from .models import PedidoImpressao, OrcamentoEvento, Pedido, Cliente, Servico

class PedidoImpressaoForm(forms.ModelForm):
    class Meta:
        model = PedidoImpressao
        fields = ['cliente', 'tamanho_foto', 'quantidade', 'preco_unitario']

class OrcamentoEventoForm(forms.ModelForm):
    class Meta:
        model = OrcamentoEvento
        fields = ['cliente', 'tipo_evento', 'data_evento', 'local_evento', 'descricao']

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'tipo_servico']         

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone', 'rua', 'bairro', 'numero', 'cidade', 'cep', 'estado']  


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['tipo_servico', 'descricao']

    # Personalize o widget para o campo 'tipo_servico'
    tipo_servico = forms.ChoiceField(
        choices=Servico.TIPO_SERVICO_OPCOES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False
    )