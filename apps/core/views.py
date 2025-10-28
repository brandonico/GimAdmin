from django.shortcuts import render,redirect
#vista basada en clases
from django.views import View

#vista basada en funciones 
from django.http import HttpResponse

#importar authenticate
from django.contrib.auth import authenticate, login, logout

#importar modelos
from .forms import CrearAsistenciaForm
from apps.abm.models import Cliente, UserProfile, Asistencia
#importar tiempo para asistencia
from django.utils import timezone
from datetime import timedelta

#importa correo
from apps.core.utils import enviar_correo
from django.contrib.auth.models import User
import random, string

def home(request):
    form = CrearAsistenciaForm()
    if request.method == 'POST':
        print(request.POST)
        form = CrearAsistenciaForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            try :
                usuario = UserProfile.objects.get(dni=dni)
            except UserProfile.DoesNotExist:
                usuario = None
                
            if not usuario:
                contexto = {
                    'mensaje': 'El usuario no está registrado en la base.',
                    'cantidad': Asistencia.objects.count(),
                    'form' : form,
                }
                return render(request, 'home.html', contexto)
            else:
                c = Cliente.objects.get(usuario=usuario)
                entrada = timezone.now()
                salida = entrada + timedelta(hours=1)
                Asistencia.objects.create(cliente=c,
                                          hora_entrada=entrada,
                                          hora_salida=salida,
                                          capacidad=100)
                #cambiar capacidad dependiendo
        
    contexto = {
        'cantidad': Asistencia.objects.count(),
        'form': form
    }
    return render(request, 'home.html', contexto)

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None : 
            login(request, user) 
            return redirect('dashboard')
        else :
            mensaje ='Usuario y/o contraseña invalido.'
            contexto = {
             'mensaje' : mensaje,

            }
            return render(request, 'login.html', contexto)
        
    contexto = {

    }
    return render(request, 'login.html', contexto)

def logoutView(request):
    logout(request)
    return redirect('home')


def dashboard(request):
    contexto = {
        'user' : request.user
    }
    return render(request, 'dashboard.html', contexto)


#implementacion de correos

def generar_contraseña_temporal(longitud=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=longitud))

def recuperar_contraseña(request):
    mensaje = ""
    if request.method == "POST":
        email = request.POST.get("email")
        try: 
            correo = User.objects.get(email=email)
            usuario = UserProfile.objects.get(user=correo)
            nueva_pass = generar_contraseña_temporal()
            correo.set_password(nueva_pass)
            correo.save()
            usuario.first_login = True
            usuario.save()
            contexto = {
                "usuario": correo.username,
                "nueva_pass": nueva_pass,
            }
            enviar_correo(
                asunto="Recuperación de contraseña",
                destinatario=email,
                contexto=str(contexto),
                plantilla_html="emails/recuperar.html"
            )
            
        
            mensaje = "Se ha enviado una nueva contraseña a tu correo."
        except User.DoesNotExist:
            mensaje = "No existe un usuario con ese correo."

    return render(request, "recuperar_contraseña.html", {"mensaje": mensaje})