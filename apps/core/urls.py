from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginView, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logoutView, name='logout'),
    path('recuperar_contraseña/', views.recuperar_contraseña, name='recuperar_contraseña'),        
    path('cambiar_password/', views.cambiar_password_primera_vez, name='cambiar_password_primera_vez'),
    path('permisos_insuficientes/', views.permisos_insuficientes, name="permisos_insuficientes"),
    path('baja_membresia/<int:pk>', views.baja_membresia, name='baja_membresia'),
    path('actualizar_membresia/<int:pk>', views.actualizar_membresia, name='actualizar_membresia')
]