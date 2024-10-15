from django.db import models

# Model para Clientes
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True)
    
    # Novos campos para endereço
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    cep = models.CharField(max_length=10)
    estado = models.CharField(max_length=2)  # Sigla do estado (ex: SP, RJ)

    def __str__(self):
        return self.nome


# Model para Pedidos de Impressão de Fotos
class PedidoImpressao(models.Model):
    TAMANHO_OPCOES = [
        ('10x15', '10x15 cm'),
        ('15x21', '15x21 cm'),
        ('20x30', '20x30 cm'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tamanho_foto = models.CharField(max_length=10, choices=TAMANHO_OPCOES)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=6, decimal_places=2)

    def calcular_total(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"Pedido de {self.cliente.nome} - {self.tamanho_foto}"

# Model para Orçamentos de Eventos
class OrcamentoEvento(models.Model):
    TIPO_EVENTO_OPCOES = [
        ('cha_revelacao', 'Chá Revelação'),
        ('cha_bebe', 'Chá de Bebê'),
        ('acompanhamento_12_meses', 'Acompanhamento 12 meses'),
        ('aniversario_1_ano', 'Aniversário 1 ano'),
        ('aniversario_outros', 'Aniversário outros'),
        ('festa_debutante', 'Festa de debutante'),
        ('formatura', 'Formatura'),
        ('pre_wedding', 'Pré-Wedding'),
        ('casamento', 'Casamento'),
        ('outros', 'Outros'),
    ]

    tipo_evento = models.CharField(
        max_length=50,
        choices=TIPO_EVENTO_OPCOES,
        default='outros'
    )
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    data_evento = models.DateField()
    local_evento = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255, default='descrição padrão')
    def __str__(self):
        return f"Orçamento para {self.get_tipo_evento_display()} - {self.cliente}"

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_evento = models.CharField(max_length=50, choices=TIPO_EVENTO_OPCOES)
    data_evento = models.DateField()
    local_evento = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255, default='descrição padrão')

    def __str__(self):
        return f"Orçamento para {self.cliente.nome} ({self.tipo_evento})"

class ServiceType(models.TextChoices):
    CHA_REVELACAO = "Chá revelação"
    CHA_BEBE = "Chá de bebê"
    ACOMPANHAMENTO_12_MESES = "Acompanhamento 12 meses"
    ANIVERSARIO_1_ANO = "Aniversário 1 ano"
    ANIVERSARIO_OUTROS = "Aniversário outros"
    FESTA_DEBUTANTE = "Festa de debutante"
    FORMATURA = "Formatura"
    PRE_WEDDING = "Pré-Wedding"
    CASAMENTO = "Casamento"
    OUTROS = "Outros"

class Pedido(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    tipo_servico = models.CharField(
        max_length=50,
        choices=ServiceType.choices,
        default=ServiceType.OUTROS
    )

class Servico(models.Model):
    TIPO_SERVICO_OPCOES = [
        ('cha_revelacao', 'Chá Revelação'),
        ('cha_bebe', 'Chá de Bebê'),
        ('acompanhamento_12_meses', 'Acompanhamento 12 meses'),
        ('aniversario_1_ano', 'Aniversário 1 ano'),
        ('aniversario_outros', 'Aniversário outros'),
        ('festa_debutante', 'Festa de debutante'),
        ('formatura', 'Formatura'),
        ('pre_wedding', 'Pré-Wedding'),
        ('casamento', 'Casamento'),
        ('outros', 'Outros'),
    ]

    tipo_servico = models.CharField(
        max_length=50,
        choices=TIPO_SERVICO_OPCOES,
        default='outros'
    )
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.get_tipo_servico_display()