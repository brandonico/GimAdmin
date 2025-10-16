from django.urls import path
from . import views

urlpatterns = [
    path('usuario/', views.usuarioAbm, name='usuarioAbm'),
    path('crearUsuario/', views.crearUsuario, name='crearUsuario'),
    path('editarUsuario/<int:pk>/', views.editarUsuario, name='editarUsuario'),
    path('eliminarUsuario/<int:pk>/', views.eliminarUsuario, name='eliminarUsuario'),
    
    path('clientes/', views.lista_clientes, name='cliente_listar'),
    path('clientes/nuevo/<int:user_id>/', views.crear_cliente, name='cliente_crear'),
    path('clientes/elegir-usuario/', views.elegir_usuario_para_cliente, name='cliente_elegir_usuario'),
    path('clientes/<int:pk>/editar/', views.editar_cliente, name='cliente_editar'),
    path('clientes/<int:pk>/eliminar/', views.eliminar_cliente, name='cliente_eliminar'),
    
    path('membresia/', views.membresiaAbm, name='membresiaAbm'),
    path('crearMembresia/', views.crearMembresia, name='crearMembresia'),
    path('editarMembresia/<int:pk>/', views.editarMembresia, name='editarMembresia'),
    path('eliminarMembresia/<int:pk>/', views.eliminarMembresia, name='eliminarMembresia'),

    path('asistencia/', views.asistenciaAbm, name='asistenciaAbm'),
    path('crearAsistencia/', views.crearAsistencia, name='crearAsistencia'),
    path('editarAsistencia/<int:pk>/', views.editarAsistencia, name='editarAsistencia'),
    path('eliminarAsistencia/<int:pk>/', views.eliminarAsistencia, name='eliminarAsistencia'),
]