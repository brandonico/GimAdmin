from django import forms
from .models import *
from django.contrib.auth.models import User

class userForm (forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

class usuarioForm (forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ['dni', 'telefono', 'domicilio', 'fecha_nac']
        widgets = {
            'fecha_nac': forms.DateInput(attrs={'type': 'date'})
        }


