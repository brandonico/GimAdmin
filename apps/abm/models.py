from django.db import models
from django.contrib.auth.models import User

class userProfile(models.Model):
    user_id = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    dni = models.IntegerField(unique=True, null=False)
    telefono = models.CharField(max_length=50)
    domicilio = models.CharField(max_length=150)
    fecha_nac = models.DateField()
    first_login = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user_id.username} - {self.dni}"

class Cliente(models.Model):
    usuario_id = models.OneToOneField(userProfile, on_delete=models.CASCADE, null=False)
    altura = models.IntegerField()
    peso = models.FloatField()
    objetivo = models.CharField(max_length=300, null=False, default="", blank=True)
    
    def __str__(self):
        return f"Cliente: {self.usuario_id.user_id.first_name} {self.usuario_id.user_id.last_name} - DNI: {self.usuario_id.dni}"

class Asistencia(models.Model):
    cliente_id = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False)
    asistencia = models.IntegerField(default=0)
    fecha_clase = models.DateField()
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()
    capacidad = models.IntegerField()

    #def __str__(self):
    #   return f"clase:"


class Membresia(models.Model):
    ESTADO_MEMBRESIA = [
        ('Activa', 'Activa'),
        ('Adeuda', 'Adeuda'),
        ('Baja'  , 'Baja'),
    ]
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, null=False)
    fecha_inicio = models.DateField(null=False)
    fecha_fin = models.DateField(null=False)
    importe = models.FloatField(null=False)
    estado = models.CharField(max_length=50, choices=ESTADO_MEMBRESIA)

    def __str__(self):
        return f"Membresia de {self.cliente}. Fecha Inicio: {self.fecha_inicio}, Fecha fin: {self.fecha_fin}, estado: {self.estado}"
