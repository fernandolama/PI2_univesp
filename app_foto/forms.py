from django import forms
from .models import PedidoImpressao, OrcamentoEvento, Cliente, Endereco, Telefone

class PedidoImpressaoForm(forms.ModelForm):
    class Meta:
        model = PedidoImpressao
        fields = ['cliente', 'tamanho_foto', 'quantidade', 'preco_unitario']

    tamanho_foto = forms.ChoiceField(
        choices=PedidoImpressao.TAMANHO_OPCOES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class OrcamentoEventoForm(forms.ModelForm):
    class Meta:
        model = OrcamentoEvento
        fields = ['cliente', 'tipo_evento', 'data_evento', 'local_evento', 'apenas_foto', 'foto_video', 'registros_impressos', 'apenas_digital', 'acabamento_simples', 'acabamento_especial' , 'outros_detalhes']

    tipo_evento = forms.ChoiceField(
        choices=OrcamentoEvento.TIPO_EVENTO_OPCOES,
        widget=forms.Select(attrs={'class': 'form-control'})
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