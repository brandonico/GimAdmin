from django.urls import path
from . import views

urlpatterns = [
    path('usuario/', views.lista_usuarios, name='usuario_listar'),
    path('usuario/nuevo', views.crear_usuario, name='usuario_crear'),
    path('usuario/<int:pk>/editar', views.editar_usuario, name='usuario_editar'),
    path('usuario/<int:pk>/eliminar', views.eliminar_usuario, name='usuario_eliminar'),
    
    path('clientes/', views.lista_clientes, name='cliente_listar'),
    path('clientes/nuevo/<int:user_id>/', views.crear_cliente, name='cliente_crear'),
    path('clientes/elegir-usuario/', views.elegir_usuario_para_cliente, name='cliente_elegir_usuario'),
    path('clientes/<int:pk>/editar/', views.editar_cliente, name='cliente_editar'),
    path('clientes/<int:pk>/eliminar/', views.eliminar_cliente, name='cliente_eliminar'),
    
    path('membresia/', views.lista_membresias, name='membresia_listar'),
    path('membresia/nueva/<int:cliente>/', views.crear_membresia, name='membresia_crear'),
    path('membresia/elegir-cliente/', views.elegir_cliente_para_membresia, name='membresia_elegir_cliente'),
    path('membresia/<int:pk>/editar/', views.editar_membresia, name='membresia_editar'),
    path('membresia/<int:pk>/eliminar/', views.eliminar_membresia, name='membresia_eliminar'),

    path('asistencia/', views.lista_asistencias, name='asistencia_listar'),
    path('asistencia/nueva/<int:cliente>/', views.crear_asistencia, name='asistencia_crear'),
    path('asistencia/elegir-cliente', views.elegir_cliente_para_asistencia, name='asistencia_elegir_cliente'),
    path('asistencia/<int:pk>/editar/', views.editar_asistencia, name='asistencia_editar'),
    path('asistencia/<int:pk>/eliminar/', views.eliminar_asistencia, name='asistencia_eliminar'),

    path('cobranza/', views.lista_cobranzas, name='cobranza_listar'),
    path('cobranza/nueva/<int:membresia>/', views.crear_cobranza, name='cobranza_crear'),
    path('cobranza/elegir-membresia/', views.elegir_membresia_para_cobranza, name="cobranza_elegir"),
    path('cobranza/<int:pk>/editar/', views.editar_cobranza, name='cobranza_editar'),
    path('cobranza/<int:pk>/eliminar/', views.eliminar_cobranza, name='cobranza_eliminar'),
]