from django.urls import path
from . import views

urlpatterns = [
    path('usuario/', views.usuarioAbm, name='usuarioAbm'),
    path('crearUsuario/', views.crearUsuario, name='crearUsuario'),
    path('editarUsuario/<int:pk>/', views.editarUsuario, name='editarUsuario'),
    path('eliminarUsuario/<int:pk>/', views.eliminarUsuario, name='eliminarUsuario'),
    
    path('cliente/', views.clienteAbm, name='clienteAbm'),
    path('crearCliente/', views.crearCliente, name='crearCliente'),
    path('editarCliente/<int:pk>/', views.editarCliente, name='editarCliente'),
    path('eliminarCliente/<int:pk>/', views.eliminarCliente, name='eliminarCliente'),

    path('membresia/', views.membresiaAbm, name='membresiaAbm'),
    path('crearMembresia/', views.crearMembresia, name='crearMembresia'),
    path('editarMembresia/<int:pk>/', views.editarMembresia, name='editarMembresia'),
    path('eliminarMembresia/<int:pk>/', views.eliminarMembresia, name='eliminarMembresia'),

    path('asistencia/', views.asistenciaAbm, name='asistenciaAbm'),
    path('crearAsistencia/', views.crearAsistencia, name='crearAsistencia'),
    path('editarAsistencia/<int:pk>/', views.editarAsistencia, name='editarAsistencia'),
    path('eliminarAsistencia/<int:pk>/', views.eliminarAsistencia, name='eliminarAsistencia'),
]