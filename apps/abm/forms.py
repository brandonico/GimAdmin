from django import forms
from .models import *
from django.contrib.auth.models import User

class userForm (forms.ModelForm):
    class Meta:
        model = User
        fields = ['password', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input mx-1'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input mx-1'}),
        }
        help_texts = {
            'username': 'Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.',
            'password': 'Requerido. Al menos 8 caracteres.',
            'is_staff': 'Designa si el usuario es Staff',
            'is_superuser': 'Designa si el usuario es Administrador (tiene todos los permisos)'
        }

class usuarioForm (forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ['dni', 'telefono', 'domicilio', 'fecha_nac']
        widgets = {
            'fecha_nac': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dni': forms.NumberInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'domicilio': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['altura', 'peso', 'objetivo', 'avatar']

class membresiaForm (forms.ModelForm):
    class Meta:
        model = Membresia
        fields = ['cliente', 'fecha_inicio', 'fecha_fin', 'importe', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'importe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ids_usados = Membresia.objects.values_list('cliente', flat=True)
        self.fields['cliente'].queryset = Cliente.objects.exclude(id__in=ids_usados)