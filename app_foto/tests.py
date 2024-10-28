from django.forms import ValidationError
from django.test import TestCase
from django.utils import timezone
from .models import Cliente, Telefone, Endereco, PedidoImpressao, TamanhoFoto, ItemPedido, OrcamentoEvento

class ClienteModelTest(TestCase):

    def setUp(self):
        # Setup para Cliente
        self.cliente = Cliente.objects.create(
            nome="João Silva",
            email="joao@example.com",
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
        )
        self.endereco = Endereco.objects.create(
            cliente=self.cliente,
            logradouro="Rua A",
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
        # Setup para Cliente, TamanhoFoto, Pedido e ItemPedido
        self.cliente = Cliente.objects.create(
            nome="Pedro Souza",
            email="pedro@example.com",
        )
        
          # Cria múltiplos tamanhos de foto
        self.tamanho_foto_10x15 = TamanhoFoto.objects.create(
            medidas="10x15",
            preco_unitario=2.50
        )
        
        self.tamanho_foto_20x30 = TamanhoFoto.objects.create(
            medidas="20x30",
            preco_unitario=5.00
        )
        
        self.tamanho_foto_30x45 = TamanhoFoto.objects.create(
            medidas="30x45",
            preco_unitario=7.50
        )

        # Cria um pedido de impressão e itens associados
        self.pedido = PedidoImpressao.objects.create(cliente=self.cliente)
        
        # Adiciona itens com diferentes tamanhos de foto ao pedido
        self.item_pedido_1 = ItemPedido.objects.create(
            pedido=self.pedido,
            tamanho_foto=self.tamanho_foto_10x15,
            quantidade=10
        )

        self.item_pedido_2 = ItemPedido.objects.create(
            pedido=self.pedido,
            tamanho_foto=self.tamanho_foto_20x30,
            quantidade=5
        )

        self.item_pedido_3 = ItemPedido.objects.create(
            pedido=self.pedido,
            tamanho_foto=self.tamanho_foto_30x45,
            quantidade=2
        )

    def test_pedido_str(self):
        """Testa a string de representação do pedido"""
        self.assertEqual(
            str(self.pedido),
            f"Pedido de {self.cliente.nome} - Total: R$ {self.pedido.calcular_total_pedido()}"
        )

    def test_calculo_total_pedido_com_multiplos_itens(self):
        """Testa o cálculo do valor total do pedido com múltiplos itens"""
        total = self.pedido.calcular_total_pedido()
        expected_total = (
            10 * 2.50 +  # 10x15
            5 * 5.00 +   # 20x30
            2 * 7.50     # 30x45
        )
        self.assertEqual(total, expected_total)

    def test_cliente_relacionado_ao_pedido(self):
        """Testa se o cliente está corretamente relacionado ao pedido"""
        self.assertEqual(self.pedido.cliente, self.cliente)
        self.assertEqual(self.pedido.cliente.nome, "Pedro Souza")

    def test_calculo_subtotal_item_pedido_1(self):
        """Testa o cálculo do subtotal para os itens do pedido 1"""
        subtotal = self.item_pedido_1.calcular_subtotal()
        self.assertEqual(subtotal, 25.00)

    def test_calculo_subtotal_item_pedido_2(self):
        """Testa o cálculo do subtotal para os itens do pedido 2S"""
        subtotal = self.item_pedido_2.calcular_subtotal()
        self.assertEqual(subtotal, 25.00)

    def test_calculo_subtotal_item_pedido_3(self):
        """Testa o cálculo do subtotal para os itens do pedido 3"""
        subtotal = self.item_pedido_3.calcular_subtotal()
        self.assertEqual(subtotal, 15.00)

'''
class OrcamentoEventoModelTest(TestCase):

    def setUp(self):
        # Setup para Cliente, Endereço e Orçamento
        self.cliente = Cliente.objects.create(
            nome="Lucas Fernandes",
            email="lucas@example.com",
        )
        self.endereco = Endereco.objects.create(
            cliente=self.cliente,
            logradouro="Rua B",
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
'''