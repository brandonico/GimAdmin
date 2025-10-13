from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginView, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logoutView, name='logout'),
    path('usuario_abm/', views.usuarioAbm, name='usuario_abm'),
    path('cliente_abm/', views.clienteAbm, name='cliente_abm'),
    path('membresia_abm/', views.membresiaAbm, name='membresia_abm'),
    path('asistencia_abm/', views.asistenciaAbm, name='asistencia_abm'),
    path('crearUsuario/', views.crearUsuario, name='crearUsuario'),
        
]