from django.shortcuts import render,redirect,get_object_or_404

from .models import userProfile, Cliente, Membresia, Asistencia
from django.contrib.auth.models import User

from .forms import usuarioForm, userForm


def usuarioAbm(request):
    contexto = {
        'user' : request.user,
        'usuarios': userProfile.objects.all()
    }
    return render(request, 'usuarioAbm.html', contexto)

def crearUsuario(request):
    if request.method == 'POST':
        user_Form = userForm(request.POST)
        usuario_Form = usuarioForm(request.POST)
        if user_Form.is_valid() and usuario_Form.is_valid():
            u = User.objects.create_user(
                username = user_Form.cleaned_data['email'],
                password = user_Form.cleaned_data['password'],
                email = user_Form.cleaned_data['email'],
                first_name = user_Form.cleaned_data['first_name'],
                last_name = user_Form.cleaned_data['last_name'],
                is_superuser = user_Form.cleaned_data['is_superuser'],
                is_staff = user_Form.cleaned_data['is_staff']
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
            return redirect('usuarioAbm')
    else:
        user_Form = userForm()
        usuario_Form = usuarioForm()
    
    contexto = {
        'user' : request.user,
        'usuarioForm': usuario_Form,
        'userForm': user_Form,
    }
    return render(request, 'crearUsuario.html', contexto)

def editarUsuario(request, pk):
    if request.method == 'POST':
        user_Form = userForm(request.POST)
        usuario_Form = usuarioForm(request.POST)
        if user_Form.is_valid() and usuario_Form.is_valid():
            u = get_object_or_404(User, pk=pk)
            uPerfil = get_object_or_404(userProfile, user_id=u)
            
            u.username = user_Form.cleaned_data['email']
            u.password = user_Form.cleaned_data['password']
            u.email = user_Form.cleaned_data['email']
            u.first_name = user_Form.cleaned_data['first_name']
            u.last_name = user_Form.cleaned_data['last_name']
            u.is_superuser = user_Form.cleaned_data['is_superuser']
            u.is_staff = user_Form.cleaned_data['is_staff']

            uPerfil.dni = usuario_Form.cleaned_data['dni']
            uPerfil.telefono = usuario_Form.cleaned_data['telefono']
            uPerfil.domicilio = usuario_Form.cleaned_data['domicilio']
            uPerfil.fecha_nac = usuario_Form.cleaned_data['fecha_nac']
            u.save()
            uPerfil.save()
            return redirect('usuarioAbm')
            
    else:

        userInstancia = get_object_or_404(User, pk=pk)
        userPerfilInstancia = get_object_or_404(userProfile, user_id=userInstancia)
        user_Form = userForm(instance=userInstancia)
        usuario_Form = usuarioForm(instance=userPerfilInstancia)
        
    contexto = {
        'user' : request.user,
        'usuarioForm': usuario_Form,
        'userForm': user_Form,
    }
    return render(request, 'crearUsuario.html', contexto)

def eliminarUsuario(request, pk):
    u = get_object_or_404(User, pk=pk)
    u.delete()
    return redirect('usuarioAbm')

def clienteAbm(request):
    contexto = {
        'clientes': Cliente.objects.all()
    }
    return render(request, 'cliente_abm.html', contexto)

def crearCliente(request):
    pass

def editarCliente(request, pk):
    pass

def eliminarCliente(request, pk):
    c = get_object_or_404(Cliente, pk=pk)
    c.delete()
    return redirect('clienteAbm')

def membresiaAbm(request):
    contexto = {
        'membresias': Membresia.objects.all()
    }
    return render(request, 'membresia_abm.html', contexto)

def crearMembresia(request):
    pass

def editarMembresia(request, pk):
    pass

def eliminarMembresia(request, pk):
    m = get_object_or_404(Membresia, pk=pk)
    m.delete()
    return redirect('membresiaAbm')

def asistenciaAbm(request):
    contexto = {
        'asistencias': Asistencia.objects.all()
    }
    return render(request, 'asistencia_abm.html', contexto)

def crearAsistencia(request):
    pass

def editarAsistencia(request, pk):
    pass

def eliminarAsistencia(request, pk):
    a = get_object_or_404(Asistencia, pk=pk)
    a.delete()
    return redirect('asistenciaAbm')
