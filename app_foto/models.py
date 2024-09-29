from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Client(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    birthday = models.DateField()

    def __str__(self):
        return f'{self.name}'

class Cellphone(BaseModel):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='cellphones')
    area_code = models.IntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(99)],
         help_text="Informe o código de área com dois dígitos (ex: 11 para São Paulo)"    
    )
    number = models.IntegerField(
        validators=[MinValueValidator(10000000), MaxValueValidator(999999999)],
        help_text="Informe o número de telefone sem o código de área"
    )

    def __str__(self):
        return f'{self.client.name} - ({self.area_code}) {self.number}'

class Address(BaseModel):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=8)
    complement = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=8)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)

    def __str__(self):
        complement_str = f' - {self.complement}' if self.complement else ''
        return f'{self.client.name} - {self.street}, {self.number}{complement_str}\n{self.zipcode} {self.city}-{self.state}'

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

class Service(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='services')
    service_type = models.CharField(
        max_length=50,
        choices=ServiceType.choices
    )
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    hour = models.TimeField()
    local = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return f'{self.client.name} - {self.get_service_type_display()}'
