from django.shortcuts import render,redirect
#vista basada en clases
from django.views import View

#vista basada en funciones 
from django.http import HttpResponse

#importar authenticate
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
            
            profile, created = UserProfile.objects.get_or_create(user=user)
            if profile.first_login:
                return redirect('cambiar_password_primera_vez')
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

@login_required
def cambiar_password_primera_vez(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user = request.user
            user.set_password(new_password)
            user.save()
            
            user.userprofile.first_login = False
            user.userprofile.save()

            update_session_auth_hash(request, user)

            messages.success(request, 'Contraseña cambiada correctamente.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')

    return render(request, 'first_login.html')

def logoutView(request):
    logout(request)
    return redirect('home')


def dashboard(request):
    contexto = {
        'user' : request.user
    }
    return render(request, 'dashboard.html', contexto)
""""
@login_required
def dashboard(request):
    # 🔹 Si es primer login, obligamos a cambiar la contraseña
    if request.user.userprofile.first_login:
        return redirect('cambiar_password_primera_vez')
        """

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
    # 🔹 Contexto normal para el dashboard
    contexto = {
        'user': request.user
    }
    return render(request, 'dashboard.html', contexto)
