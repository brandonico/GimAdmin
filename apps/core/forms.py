from django import forms
from datetime import date,timedelta
from django.conf import settings

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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #rellena la form con la fecha de hoy, 30 dias de hoy, precio en settings y activa por defecto.
        fecha_hoy = date.today()
        self.fields['fecha_inicio'].initial = fecha_hoy
        self.fields['fecha_fin'].initial = fecha_hoy + timedelta(days=30)
        self.fields['importe'].initial = settings.PRECIO_MES_SUSCRIPCION
        self.fields['estado'].initial = 'Activa'