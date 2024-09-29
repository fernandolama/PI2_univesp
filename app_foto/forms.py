from django import forms
from django.forms import inlineformset_factory
from .models import Address, Cellphone, Client, Service

class ClientForm(forms.ModelForm):
    birthday = forms.DateField(
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'}),
        input_formats=['%d-%m-%Y']
    )
    class Meta:
        model = Client
        fields = '__all__'

class CellphoneForm(forms.ModelForm):
    class Meta:
        model = Cellphone
        fields = ['area_code', 'number']
        widgets = {
            'area_code': forms.TextInput(attrs={
                'class': 'simple-input',
                'placeholder': 'DDD'
            }),
            'number': forms.TextInput(attrs={
                'class': 'simple-input',
                'placeholder': 'XXXXXXXXX'
            })
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'number', 'complement', 'zipcode', 'city', 'state']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['client', 'service_type', 'description', 'date', 'hour', 'local']


CellphoneFormSet = inlineformset_factory(Client, Cellphone, fields=('area_code', 'number'), extra=1)
AddressFormSet = inlineformset_factory(Client, Address, fields=('street', 'number', 'complement', 'zipcode', 'city', 'state'), extra=1)