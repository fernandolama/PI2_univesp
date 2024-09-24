from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Client(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    
class Cellphone(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='cellphones')
    area_code = models.IntegerField(max_length=2)
    number = models.IntegerField(max_length=9)
    
class Address(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=100)
    number = models.IntegerField(max_length=8)
    complement = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.IntegerField(max_length=8)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)