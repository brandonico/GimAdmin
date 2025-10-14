from django.shortcuts import render,redirect
#vista basada en clases
from django.views import View

#vista basada en funciones 
from django.http import HttpResponse

#importar authenticate
from django.contrib.auth import authenticate, login, logout

#importar modelos
    
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
        'user' : request.user
    }
    return render(request, 'dashboard.html', contexto)


