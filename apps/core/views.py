from django.shortcuts import render,redirect
# Create your views here.
#vista basada en clases
from django.views import View

#vista basada en funciones 
from django.http import HttpResponse

#importar authenticate
from django.contrib.auth import authenticate, login, logout

#importar modelos
from .models import userProfile, Cliente, Membresia, Asistencia
from django.contrib.auth.models import User

from .forms import usuarioForm, userForm
    
def home(request):
    contexto= {
        'cantidad': 10
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
    if request.method == 'POST':
        user_Form = userForm(request.POST)
        usuario_Form = usuarioForm(request.POST)
        contexto = {
            'user' : request.user,
            'usuarios': userProfile.objects.all(),
            'clientes': Cliente.objects.all(),
            'membresias': Membresia.objects.all(),
            'asistencias': Asistencia.objects.all(),
            'usuarioForm': usuario_Form,
            'userForm': user_Form
        }
        if user_Form.is_valid() and usuario_Form.is_valid():
            u = User.objects.create_user(
                username = user_Form.cleaned_data['username'],
                password = user_Form.cleaned_data['password'],
                email = user_Form.cleaned_data['email'],
                first_name = user_Form.cleaned_data['first_name'],
                last_name = user_Form.cleaned_data['last_name']
            )
            uPerfil = userProfile.objects.create(
                user_id = u,
                dni = usuario_Form.cleaned_data['dni'],
                telefono = usuario_Form.cleaned_data['telefono'],
                domicilio = usuario_Form.cleaned_data['domicilio'],
                fecha_nac = usuario_Form.cleaned_data['fecha_nac']
            )
            u.save()
            uPerfil.save()

            return redirect('dashboard')
    else:
        user_Form = userForm()
        usuario_Form = usuarioForm()
        contexto = {
            'user' : request.user,
            'usuarios': userProfile.objects.all(),
            'clientes': Cliente.objects.all(),
            'membresias': Membresia.objects.all(),
            'asistencias': Asistencia.objects.all(),
            'usuarioForm': usuario_Form,
            'userForm': user_Form
        }
    return render(request, 'dashboard.html', contexto)

def usuarioAbm(request):
    if request.method == 'POST':
        user_Form = userForm(request.POST)
        usuario_Form = usuarioForm(request.POST)
        contexto = {
            'user' : request.user,
            'usuarios': userProfile.objects.all(),
            'usuarioForm': usuario_Form,
            'userForm': user_Form
        }
        if user_Form.is_valid() and usuario_Form.is_valid():
            u = User.objects.create_user(
                username = user_Form.cleaned_data['username'],
                password = user_Form.cleaned_data['password'],
                email = user_Form.cleaned_data['email'],
                first_name = user_Form.cleaned_data['first_name'],
                last_name = user_Form.cleaned_data['last_name']
            )
            uPerfil = userProfile.objects.create(
                user_id = u,
                dni = usuario_Form.cleaned_data['dni'],
                telefono = usuario_Form.cleaned_data['telefono'],
                domicilio = usuario_Form.cleaned_data['domicilio'],
                fecha_nac = usuario_Form.cleaned_data['fecha_nac']
            )
            u.save()
            uPerfil.save()

            return redirect('dashboard')
    else:
        user_Form = userForm()
        usuario_Form = usuarioForm()
        contexto = {
            'user' : request.user,
            'usuarios': userProfile.objects.all(),
            'usuarioForm': usuario_Form,
            'userForm': user_Form
        }
    return render(request, 'usuario_abm.html', contexto)

def crearUsuario(request):
    if request.method == 'POST':
        user_Form = userForm(request.POST)
        usuario_Form = usuarioForm(request.POST)
        contexto = {
            'user' : request.user,
            'usuarioForm': usuario_Form,
            'userForm': user_Form
        }
        if user_Form.is_valid() and usuario_Form.is_valid():
            u = User.objects.create_user(
                username = user_Form.cleaned_data['username'],
                password = user_Form.cleaned_data['password'],
                email = user_Form.cleaned_data['email'],
                first_name = user_Form.cleaned_data['first_name'],
                last_name = user_Form.cleaned_data['last_name']
            )
            uPerfil = userProfile.objects.create(
                user_id = u,
                dni = usuario_Form.cleaned_data['dni'],
                telefono = usuario_Form.cleaned_data['telefono'],
                domicilio = usuario_Form.cleaned_data['domicilio'],
                fecha_nac = usuario_Form.cleaned_data['fecha_nac']
            )
            u.save()
            uPerfil.save()

            return redirect('usuario_abm')
    else:
        user_Form = userForm()
        usuario_Form = usuarioForm()
        contexto = {
            'user' : request.user,
            'usuarioForm': usuario_Form,
            'userForm': user_Form
        }
    return render(request, 'crearUsuario.html', contexto)

def clienteAbm(request):
    contexto = {
        'clientes': Cliente.objects.all()
    }
    return render(request, 'cliente_abm.html', contexto)

def membresiaAbm(request):
    contexto = {
        'membresias': Membresia.objects.all()
    }
    return render(request, 'membresia_abm.html', contexto)  

def asistenciaAbm(request):
    contexto = {
        'asistencias': Asistencia.objects.all()
    }
    return render(request, 'asistencia_abm.html', contexto)

