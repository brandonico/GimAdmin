from django.db import models

class Provincia(models.Model):
    descripcion = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descripcion


class Localidad(models.Model):
    descripcion = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT, related_name="localidades")

    class Meta:
        unique_together = ('descripcion', 'provincia')  
        
    def __str__(self):
        return f"{self.descripcion} ({self.provincia})"


class Domicilio(models.Model):
    calle = models.CharField(max_length=120)
    numero = models.CharField(max_length=10, blank=True, null=True)
    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT, related_name="domicilios")
    codigo_postal = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.calle} {self.numero or ''}, {self.localidad}"


class Persona(models.Model):
    apellido = models.CharField(max_length=80)
    nombre = models.CharField(max_length=80)
    dni = models.CharField("Documento", max_length=20, blank=True, null=True, unique=True)
    fecha_nacimiento = models.DateField()
    domicilio = models.ForeignKey(Domicilio, on_delete=models.SET_NULL, null=True, blank=True, related_name="personas")
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      

    class Meta:
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"