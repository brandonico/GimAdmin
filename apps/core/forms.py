from django import forms

class CrearAsistenciaForm (forms.Form):
    dni = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}))

class ActualizarMembresiaForm(forms.Form):
    ESTADO_MEMBRESIA = [
        ('Activa', 'Activa'),
        ('Adeuda', 'Adeuda'),
        ('Baja', 'Baja'),
    ]
    METODO_PAGO = [
        ('Efectivo','Efectivo'),
        ('Tarjeta','Tarjeta'),
        ('Transferencia', 'Transferencia')
    ]
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    estado = forms.ChoiceField(choices=ESTADO_MEMBRESIA, widget=forms.Select(attrs={'class': 'form-control'}))
    importe = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))
    metodo_pago = forms.ChoiceField(choices=METODO_PAGO, widget=forms.Select(attrs={'class': 'form-control'}))