from django.urls import path
from . import views

urlpatterns = [
    path('usuario/', views.usuarioAbm, name='usuarioAbm'),
    path('crearUsuario/', views.crearUsuario, name='crearUsuario'),
    path('editarUsuario/<int:id>/', views.editarUsuario, name='editarUsuario'),
    path('eliminarUsuario/<int:id>/', views.eliminarUsuario, name='eliminarUsuario'),
    
    path('cliente/', views.clienteAbm, name='clienteAbm'),
    path('membresia/', views.membresiaAbm, name='membresiaAbm'),
    path('asistencia/', views.asistenciaAbm, name='asistenciaAbm')
        
]