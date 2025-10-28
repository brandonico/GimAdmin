from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginView, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logoutView, name='logout'),
    path('recuperar_contraseña/', views.recuperar_contraseña, name='recuperar_contraseña'),        
]