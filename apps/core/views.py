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


