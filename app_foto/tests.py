from django.forms import ValidationError
from django.test import TestCase
from .models import Cliente, Telefone, Endereco, PedidoImpressao, TamanhoFoto, ItemPedido, OrcamentoEvento, TipoEvento, RecursoEvento
from datetime import time, date

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

class TipoEventoModelTest(TestCase):
    def setUp(self):
        self.tipo_evento = TipoEvento.objects.create(nome="Casamento", preco=3000.00)

    def test_tipo_evento_str(self):
        self.assertEqual(str(self.tipo_evento), "Casamento")

    def test_tipo_evento_unique_name(self):
        with self.assertRaises(Exception):
            TipoEvento.objects.create(nome="Casamento", preco=1500.00)

class RecursoEventoModelTest(TestCase):
    def setUp(self):
        self.recurso_evento = RecursoEvento.objects.create(nome="Foto+Vídeo", preco=1200.00)

    def test_recurso_evento_str(self):
        self.assertEqual(str(self.recurso_evento), "Foto+Vídeo")

    def test_recurso_evento_unique_name(self):
        with self.assertRaises(Exception):
            RecursoEvento.objects.create(nome="Foto+Vídeo", preco=1000.00)

class OrcamentoEventoModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nome="João", email="joao@example.com")
        self.tipo_evento = TipoEvento.objects.create(nome="Aniversário", preco=2000.00)
        self.recurso_evento = RecursoEvento.objects.create(nome="Foto+Vídeo", preco=1000.00)
        self.orcamento_evento = OrcamentoEvento.objects.create(
            cliente=self.cliente,
            tipo_evento=self.tipo_evento,
            data_evento=date.today(),
            hora_evento=time(18, 0),
            local_evento="Salão de Festas",
            logradouro="Rua dos Bobos",
            numero="0",
            bairro="Jardim",
            cep="12345-678",
            cidade="São Paulo",
            estado="SP"
        )
        self.orcamento_evento.recursos_adicionais.add(self.recurso_evento)

    def test_orcamento_evento_str(self):
        self.assertEqual(
            str(self.orcamento_evento),
            f"Orçamento para {self.tipo_evento} - {self.cliente}: R$ {self.orcamento_evento.calcular_total_evento()}"
        )

    def test_calcular_total_evento(self):
        total = self.orcamento_evento.calcular_total_evento()
        self.assertEqual(total, 3000.00)  # 2000 (tipo_evento) + 1000 (recurso_evento)

    def test_orcamento_evento_relations(self):
        self.assertEqual(self.orcamento_evento.cliente.nome, "João")
        self.assertEqual(self.orcamento_evento.tipo_evento.nome, "Aniversário")
        self.assertIn(self.recurso_evento, self.orcamento_evento.recursos_adicionais.all())
