import enum
from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Client(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    birthday = models.DateField()

    def __str__(self):
        return f'{self.name}'
    
class Cellphone(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='cellphones')
    area_code = models.IntegerField(max_length=2)
    number = models.IntegerField(max_length=9)

    def __str__(self):
        return f'{self.client.name} - ({self.area_code}) {self.number}'
    
class Address(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=100)
    number = models.IntegerField(max_length=8)
    complement = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.IntegerField(max_length=8)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)

    def __str__(self):
        return f'{self.client.name} - {self.street}, {self.number} - {self.complement}\n{self.zipcode} {self.city}-{self.state}'

class ServiceType(enum.Enum):
    CHA_REVELACAO = "Chá revelação"
    CHA_BEBE = "Chá de bebê"
    ACOMPANHAMENTO_12_MESES = "Acompanhamento_12 meses"
    ANIVERSARIO_1_ANO = "Aniversário_1 ano"
    ANIVERSARIO_OUTROS = "Aniversário_outros"
    FESTA_DEBUTANTE = "Festa de debutante"
    PRE_WEDDING = "Pré-Wedding"
    CASAMENTO = "Casamento"
    OUTROS = "Outros"

class Service(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='services')
    service_type = models.CharField(
        max_length=50,
        choices=[(tag.name, tag.value) for tag in ServiceType]
    )
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    hour = models.TimeField()
    local = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return f'{self.client.name} - {self.get_service_type_display()}'