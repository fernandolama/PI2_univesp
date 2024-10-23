from django.forms import ValidationError
from django.test import TestCase
from django.utils import timezone
from .models import Cliente, Telefone, Endereco, PedidoImpressao, OrcamentoEvento

class ClienteModelTest(TestCase):

    def setUp(self):
        # Setup para Cliente
        self.cliente = Cliente.objects.create(
            nome="João Silva",
            email="joao@example.com",
            data_nascimento="1990-01-01"
        )

    def test_cliente_str(self):
        """Testa a string de representação do cliente"""
        self.assertEqual(str(self.cliente), "João Silva")
    
    def test_cliente_nome_required(self):
        """
        Teste para garantir que o campo 'nome' seja obrigatório.
        """
        cliente = Cliente.objects.create(
            nome="",
            email="teste@example.com",
            data_nascimento="1995-10-10"
        )
        with self.assertRaises(ValidationError):
            cliente.full_clean()


    def test_cliente_telefone(self):
        """Testa a criação e ligação de um telefone ao cliente"""
        telefone = Telefone.objects.create(
            cliente=self.cliente,
            codigo_area=11,
            numero=987654321
        )
        self.assertEqual(str(telefone), "João Silva - (11) 987654321")


class EnderecoModelTest(TestCase):

    def setUp(self):
        # Setup para Cliente e Endereço
        self.cliente = Cliente.objects.create(
            nome="Maria Oliveira",
            email="maria@example.com",
            data_nascimento="1985-05-15"
        )
        self.endereco = Endereco.objects.create(
            cliente=self.cliente,
            rua="Rua A",
            numero="123",
            bairro="Centro",
            cep="12345678",
            cidade="São Paulo",
            estado="SP"
        )

    def test_endereco_str(self):
        """Testa a string de representação do endereço"""
        self.assertEqual(
            str(self.endereco),
            "Maria Oliveira - Rua A, 123\nCentro 12345678\nSão Paulo-SP"
        )


class PedidoImpressaoModelTest(TestCase):

    def setUp(self):
        # Setup para Cliente e Pedido
        self.cliente = Cliente.objects.create(
            nome="Pedro Souza",
            email="pedro@example.com",
            data_nascimento="1992-02-20"
        )
        self.pedido = PedidoImpressao.objects.create(
            cliente=self.cliente,
            tamanho_foto='10x15',
            quantidade=10,
            preco_unitario=2.50
        )

    def test_pedido_str(self):
        """Testa a string de representação do pedido"""
        self.assertEqual(
            str(self.pedido),
            "Pedido de Pedro Souza - R$ 25.0"
        )

    def test_calculo_total_pedido(self):
        """Testa o cálculo do valor total do pedido"""
        total = self.pedido.calcular_total_pedido()
        self.assertEqual(total, 25.00)


class OrcamentoEventoModelTest(TestCase):

    def setUp(self):
        # Setup para Cliente, Endereço e Orçamento
        self.cliente = Cliente.objects.create(
            nome="Lucas Fernandes",
            email="lucas@example.com",
            data_nascimento="1988-08-08"
        )
        self.endereco = Endereco.objects.create(
            cliente=self.cliente,
            rua="Rua B",
            numero="456",
            bairro="Jardins",
            cep="87654321",
            cidade="Rio de Janeiro",
            estado="RJ"
        )
        self.orcamento = OrcamentoEvento.objects.create(
            cliente=self.cliente,
            tipo_evento='casamento',
            data_evento="2024-12-12",
            local_evento=self.endereco,
            apenas_foto=False,
            foto_video=True,
            registros_impressos=True,
            apenas_digital=False,
            acabamento_simples=False,
            acabamento_especial=True,
        )

    def test_orcamento_str(self):
        """Testa a string de representação do orçamento"""
        self.assertEqual(
            str(self.orcamento),
            "Orçamento para Casamento - Lucas Fernandes: R$ 4650.0"
        )

    def test_calculo_total_evento(self):
        """Testa o cálculo do valor total do orçamento"""
        total = self.orcamento.calcular_total_evento()
        self.assertEqual(total, 4650.0)
