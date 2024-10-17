from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Model para Clientes
class Cliente(BaseModel):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField()
    
    def __str__(self):
        return f'{self.nome}'

class Telefone(BaseModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='telefones')
    codigo_area = models.IntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(99)],
         help_text="Informe o código de área com dois dígitos (ex: 11 para São Paulo)"    
    )
    numero = models.IntegerField(
        validators=[MinValueValidator(10000000), MaxValueValidator(999999999)],
        help_text="Informe o número de telefone sem o código de área"
    )

    def __str__(self):
        return f'{self.cliente.nome} - ({self.codigo_area}) {self.numero}'


class Endereco(BaseModel):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='enderecos')
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=8)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2)

    def __str__(self):
        complemento_str = f' - {self.complemento}' if self.complemento else ''
        return f'{self.cliente.nome} - {self.rua}, {self.numero}\n{complemento_str}\n{self.bairro} {self.cep}\n{self.cidade}-{self.estado}'
    

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