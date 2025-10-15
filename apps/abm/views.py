from django.shortcuts import render,redirect,get_object_or_404

from .models import userProfile, Cliente, Membresia, Asistencia
from django.contrib.auth.models import User

from .forms import usuarioForm, userForm, userTipoForm


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
        userTipo_Form = userTipoForm(request.POST)
        if user_Form.is_valid() and usuario_Form.is_valid():
            if userTipo_Form.is_valid():
                isAdmin = userTipo_Form.cleaned_data['is_superuser']
                isStaff = userTipo_Form.cleaned_data['is_staff']
            else:
                isAdmin = False
                isStaff = False
            u = User.objects.create_user(
                username = user_Form.cleaned_data['email'],
                password = user_Form.cleaned_data['password'],
                email = user_Form.cleaned_data['email'],
                first_name = user_Form.cleaned_data['first_name'],
                last_name = user_Form.cleaned_data['last_name'],
                is_superuser = isAdmin,
                is_staff = isStaff
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
        userTipo_Form = userTipoForm()
    
    contexto = {
        'user' : request.user,
        'usuarioForm': usuario_Form,
        'userForm': user_Form,
        'userTipoForm': userTipo_Form
    }
    return render(request, 'crearUsuario.html', contexto)

def editarUsuario(request, pk):
    if request.method == 'POST':
        user_Form = userForm(request.POST)
        usuario_Form = usuarioForm(request.POST)
        userTipo_Form = userTipoForm(request.POST)
        if user_Form.is_valid() and usuario_Form.is_valid():
            if userTipo_Form.is_valid():
                isAdmin = userTipo_Form.cleaned_data['is_superuser']
                isStaff = userTipo_Form.cleaned_data['is_staff']
            else:
                isAdmin = False
                isStaff = False
            u = User.objects.create_user(
                username = user_Form.cleaned_data['email'],
                password = user_Form.cleaned_data['password'],
                email = user_Form.cleaned_data['email'],
                first_name = user_Form.cleaned_data['first_name'],
                last_name = user_Form.cleaned_data['last_name'],
                is_superuser = isAdmin,
                is_staff = isStaff
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
        userInstancia = get_object_or_404(User, pk=pk)
        userPerfilInstancia = get_object_or_404(userProfile, user_id=pk)
        userTipoInstancia = get_object_or_404(User, pk=pk)
        user_Form = userForm(instance=userInstancia)
        usuario_Form = usuarioForm(instance=userPerfilInstancia)
        userTipo_Form = userTipoForm(instance=userTipoInstancia)
        
    contexto = {
        'user' : request.user,
        'usuarioForm': usuario_Form,
        'userForm': user_Form,
        'userTipoForm': userTipo_Form
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
