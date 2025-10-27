from django.urls import path
from . import views

urlpatterns = [
    path('usuario/', views.lista_usuarios, name='usuarioAbm'),
    path('crearUsuario/', views.crear_usuario, name='crearUsuario'),
    path('editarUsuario/<int:pk>/', views.editar_usuario, name='editarUsuario'),
    path('eliminarUsuario/<int:pk>/', views.eliminar_usuario, name='eliminarUsuario'),
    
    path('clientes/', views.lista_clientes, name='cliente_listar'),
    path('clientes/nuevo/<int:user_id>/', views.crear_cliente, name='cliente_crear'),
    path('clientes/elegir-usuario/', views.elegir_usuario_para_cliente, name='cliente_elegir_usuario'),
    path('clientes/<int:pk>/editar/', views.editar_cliente, name='cliente_editar'),
    path('clientes/<int:pk>/eliminar/', views.eliminar_cliente, name='cliente_eliminar'),
    
    path('membresia/', views.lista_membresias, name='membresiaAbm'),
    path('crearMembresia/', views.crear_membresia, name='crearMembresia'),
    path('membresia/elegir-cliente', views.elegir_cliente_para_membresia, name='membresia_elegir_cliente'),
    path('editarMembresia/<int:pk>/', views.editar_membresia, name='editarMembresia'),
    path('eliminarMembresia/<int:pk>/', views.eliminar_membresia, name='eliminarMembresia'),

    path('asistencia/', views.lista_asistencias, name='asistenciaAbm'),
    path('crearAsistencia/', views.crear_asistencia, name='crearAsistencia'),
    path('editarAsistencia/<int:pk>/', views.editar_asistencia, name='editarAsistencia'),
    path('eliminarAsistencia/<int:pk>/', views.eliminar_asistencia, name='eliminarAsistencia'),

    path('cobranza/', views.lista_cobranzas, name='cobranzaAbm'),
    path('crearCobranza/', views.crear_cobranza, name='crearCobranza'),
    path('editarCobranza/<int:pk>/', views.editar_cobranza, name='editarCobranza'),
    path('eliminarCobranza/<int:pk>/', views.eliminar_cobranza, name='eliminarCobranza'),
]