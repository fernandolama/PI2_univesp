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
    
    def __str__(self):
        return f'{self.nome}'

class Telefone(BaseModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='telefones')
    codigo_area = models.IntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(99)],
        blank=True, null=True     
    )
    numero = models.IntegerField(
        validators=[MinValueValidator(10000000), MaxValueValidator(999999999)],
        blank=True, null=True
    )

    def __str__(self):
        return f'{self.cliente.nome} - ({self.codigo_area}) {self.numero}'


class Endereco(BaseModel):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='enderecos')
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=8)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2)

    def __str__(self):
        complemento_str = f' - {self.complemento}\n' if self.complemento else ''
        return f'{self.cliente.nome} - {self.logradouro}, {self.numero}\n{complemento_str}{self.bairro} {self.cep}\n{self.cidade}-{self.estado}'
    
class TamanhoFoto(BaseModel):
    medidas = models.CharField(max_length=20, unique=True)
    preco_unitario = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.medidas} - R$ {self.preco_unitario}'

class PedidoImpressao(BaseModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="pedidos")
    
    def calcular_total_pedido(self):
        total = sum(item.calcular_subtotal() for item in self.itens.all())
        return total

    def __str__(self):
        return f"Pedido de {self.cliente.nome} - Total: R$ {self.calcular_total_pedido()}"


class ItemPedido(BaseModel):
    pedido = models.ForeignKey(PedidoImpressao, on_delete=models.CASCADE, related_name='itens')
    tamanho_foto = models.ForeignKey(TamanhoFoto, on_delete=models.CASCADE, related_name='itens')
    quantidade = models.PositiveIntegerField()
    
    def calcular_subtotal(self):
        return self.quantidade * self.tamanho_foto.preco_unitario

    def __str__(self):
        return f"{self.quantidade} foto(s) no tamanho {self.tamanho_foto.medidas}: R$ {self.calcular_subtotal()}"
        
class TipoEvento(BaseModel):
    nome = models.CharField(max_length=50, unique=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2, help_text="Preço para este tipo de evento")

    def __str__(self):
        return f"{self.nome}"
    
class RecursoEvento(BaseModel):
    nome = models.CharField(max_length=100, unique=True, help_text="Nome do recurso adicional")
    preco = models.DecimalField(max_digits=8, decimal_places=2, help_text="Preço para este recurso")
    
    def __str__(self):
        return self.nome

class OrcamentoEvento(BaseModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="eventos")
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.CASCADE, related_name="orcamentos")
    data_evento = models.DateField()
    hora_evento = models.TimeField()
    local_evento = models.ForeignKey(Endereco, on_delete=models.CASCADE, related_name="eventos")
    recursos_adicionais = models.ManyToManyField(RecursoEvento, related_name="orcamentos", blank=True)
    outros_detalhes = models.CharField(max_length=500, blank=True, null=True)
    
    def calcular_total_evento(self):
        # Iniciar com o preço base do tipo de evento
        total = self.tipo_evento.preco

        # Somar preços dos recursos adicionais
        for recurso in self.recursos_adicionais.all():
            total += recurso.preco

        return total
        
    def __str__(self):
        return f"Orçamento para {self.tipo_evento} - {self.cliente}: R$ {self.calcular_total_evento()}"