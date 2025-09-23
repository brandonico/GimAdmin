from django.shortcuts import render,redirect
# Create your views here.
#vista basada en clases
from django.views import View

#vista basada en funciones 
from django.http import HttpResponse

#importar authenticate
from django.contrib.auth import authenticate, login, logout

def hola_mundo (request):
    return HttpResponse ("Hola Mundo desde una vista basada en funcion")

#vista basada en clases
class HolaMundoView(View):
    def get(self, request):
        return HttpResponse("Hola Mundo desde una vista basada en clases")
    
def Index(request):
    contexto = {
        'mensaje': 'Bienvenidos a GymAdmin',
        'nombre' : 'PEPE',
        'edad' : '30'
    }
    return render(request, 'index.html', contexto)


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
    contexto = {
        'user' : request.user,
    }
    return render(request, 'dashboard.html', contexto)