from django import forms
from .models import *
from django.contrib.auth.models import User

class userForm (forms.ModelForm):
    class Meta:
        model = User
        fields = ['password', 'email', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput(),
        }
        help_texts = {
            'username': 'Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.',
            'password': 'Requerido. Al menos 8 caracteres.'
        }

class userTipoForm (forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_staff', 'is_superuser']
        widgets = {
            'is_staff': forms.CheckboxInput(),
            'is_superuser': forms.CheckboxInput(),
        }
        help_texts = {
            'is_staff': 'Designa si el usuario es Staff',
            'is_superuser': 'Designa si el usuario es Administrador (tiene todos los permisos)'
        }
        labels = {
            'is_staff': 'Es Staff',
            'is_superuser': 'Es Admin'
        }

class usuarioForm (forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ['dni', 'telefono', 'domicilio', 'fecha_nac']
        widgets = {
            'fecha_nac': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class clienteForm (forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['altura', 'peso', 'objetivo']