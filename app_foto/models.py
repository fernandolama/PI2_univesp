from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
        complemento_str = f' - {self.complemento}\n' if self.complemento else ''
        return f'{self.cliente.nome} - {self.rua}, {self.numero}\n{complemento_str}{self.bairro} {self.cep}\n{self.cidade}-{self.estado}'
    

# Model para Pedidos de Impressão de Fotos
class PedidoImpressao(models.Model):
    TAMANHO_OPCOES = [
        ('10x15', '10x15 cm'),
        ('15x21', '15x21 cm'),
        ('20x30', '20x30 cm'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="pedidos")
    tamanho_foto = models.CharField(max_length=10, choices=TAMANHO_OPCOES)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=6, decimal_places=2)

    def calcular_total_pedido(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"Pedido de {self.cliente.nome} - R$ {self.calcular_total_pedido()}"

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
        ('corporativo', 'Evento corporativo'),
        ('outros', 'Outros'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="eventos")
    tipo_evento = models.CharField(
        max_length=50,
        choices=TIPO_EVENTO_OPCOES,
        default='outros'
    )
    data_evento = models.DateField()
    local_evento = models.ForeignKey(Endereco, on_delete=models.CASCADE, related_name="eventos")
    apenas_foto = models.BooleanField(default=False, verbose_name="Apenas foto?")
    foto_video = models.BooleanField(default=False, verbose_name="Foto e vídeo?")
    registros_impressos = models.BooleanField(default=False, verbose_name="Registros impressos?")
    apenas_digital = models.BooleanField(default=False, verbose_name="Apenas digital?")
    acabamento_simples = models.BooleanField(default=False, verbose_name="Acabamento do álbum simples?")
    acabamento_especial = models.BooleanField(default=False, verbose_name="Acabamento do álbum especial?")
    outros_detalhes = models.CharField(max_length=500, blank=True, null=True)
    
    PRECO_TIPO_EVENTO = {
        'cha_revelacao': 500.0,
        'cha_bebe': 400.0,
        'acompanhamento_12_meses': 100.0,
        'aniversario_1_ano': 800.0,
        'aniversario_outros': 700.0,
        'festa_debutante': 1500.0,
        'formatura': 1300.0,
        'pre_wedding': 1000.0,
        'casamento': 3000.0,
        'corporativo': 2000.0,
        'outros': 600.0,
    }

    def calcular_total_evento(self):
        # Iniciar com o preço base do tipo de evento
        total = self.PRECO_TIPO_EVENTO.get(self.tipo_evento, 0)

        # Adicionar valores adicionais com base nas opções selecionadas
        if self.apenas_foto:
            total += 500 
        if self.foto_video:
            total += 1000
        if self.registros_impressos:
            total += 300 
        if self.apenas_digital:
            total += 200 
        if self.acabamento_simples:
            total += 150 
        if self.acabamento_especial:
            total += 350 

        return total
        
    def __str__(self):
        return f"Orçamento para {self.get_tipo_evento_display()} - {self.cliente}: R$ {self.calcular_total_evento()}"