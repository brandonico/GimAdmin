from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Cliente)
admin.site.register(Membresia)
admin.site.register(Asistencia)
admin.site.register(Cobranza)
