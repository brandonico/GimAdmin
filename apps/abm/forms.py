from django import forms
from .models import *
from django.contrib.auth.models import User

class userForm (forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput(),
        }

class userTipoForm (forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_staff', 'is_superuser']
        widgets = {
            'is_staff': forms.CheckboxInput(),
            'is_superuser': forms.CheckboxInput(),
        }

class usuarioForm (forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ['dni', 'telefono', 'domicilio', 'fecha_nac']
        widgets = {
            'fecha_nac': forms.DateInput(attrs={'type': 'date'})
        }

class clienteForm (forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['altura', 'peso', 'objetivo']