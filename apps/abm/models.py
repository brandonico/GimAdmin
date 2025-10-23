from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    dni = models.IntegerField(unique=True, null=False)
    telefono = models.CharField(max_length=50)
    domicilio = models.CharField(max_length=150)
    fecha_nac = models.DateField()
    first_login = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.dni}"

class Cliente(models.Model):
    usuario = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=False, related_name='cliente_usuario')
    altura = models.IntegerField()
    peso = models.FloatField()
    objetivo = models.CharField(max_length=300, null=False, default="", blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default.jpg')
    
    def __str__(self):
        return f"Cliente: {self.usuario.user.first_name} {self.usuario.user.last_name} - DNI: {self.usuario.dni}"

class Asistencia(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False)
    fecha_clase = models.DateField(auto_now_add=True)
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
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, null=False, related_name='membresia_cliente')
    fecha_inicio = models.DateField(null=False)
    fecha_fin = models.DateField(null=False)
    estado = models.CharField(max_length=50, choices=ESTADO_MEMBRESIA)

    def __str__(self):
        return f"Membresia de {self.cliente}. Fecha Inicio: {self.fecha_inicio}, Fecha fin: {self.fecha_fin}, estado: {self.estado}"

class Cobranza(models.Model):
    METODO_PAGO = [
        ('Efectivo','Efectivo'),
        ('Tarjeta','Tarjeta'),
        ('Transferencia', 'Transferencia')
    ]
    fecha_pago = models.DateField(auto_now_add=True)
    importe = models.FloatField(null=False)
    membresia = models.ForeignKey(Membresia, on_delete=models.CASCADE, null=False, related_name='membresia')
    metodo_pago = models.CharField(max_length=30, choices=METODO_PAGO)

    def __str__(self):
        return f"Cobranza de {self.membresia}, {self.fecha_pago}, {self.importe}"
