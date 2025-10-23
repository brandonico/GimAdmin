from django import forms

class CrearAsistenciaForm (forms.Form):
    dni = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}))
    