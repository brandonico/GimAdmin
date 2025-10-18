from django.shortcuts import render, redirect, get_object_or_404
from django.forms import HiddenInput

from .models import userProfile, Cliente, Membresia, Asistencia
from django.contrib.auth.models import User

from .forms import usuarioForm, userForm, ClienteForm, membresiaForm

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
    u = get_object_or_404(User, pk=pk)
    uPerfil = get_object_or_404(userProfile, user_id=pk)
    if request.method == 'POST':    
        user_Form = userForm(request.POST, instance=u)
        usuario_Form = usuarioForm(request.POST, instance=uPerfil)
        if user_Form.is_valid() and usuario_Form.is_valid():
            u = user_Form.save(commit=False)
            uPerfil = usuario_Form.save(commit=False)
            u.save()
            uPerfil.save()
            return redirect('usuarioAbm')
    else:
        user_Form = userForm(instance=u)
        usuario_Form = usuarioForm(instance=uPerfil)
    contexto = {
        'user' : request.user,
        'usuarioForm': usuario_Form,
        'userForm': user_Form,
    }
    return render(request, 'crearUsuario.html', contexto)

def eliminarUsuario(pk):
    u = get_object_or_404(User, pk=pk)
    u.delete()
    return redirect('usuarioAbm')

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'lista_clientes.html', {'clientes': clientes})

def crear_cliente(request, user_id):
    perfil = get_object_or_404(userProfile, pk=user_id)

    if Cliente.objects.filter(usuario_id=perfil).exists():
        return redirect('cliente_listar')

    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario_id = perfil
            cliente.save()
            return redirect('cliente_listar')
    else:
        form = ClienteForm()
    return render(request, 'crear_cliente.html', {'form': form, 'perfil': perfil})

def elegir_usuario_para_cliente(request):
    perfiles = userProfile.objects.all()
    return render(request, 'elegir_usuario.html', {'perfiles': perfiles})

def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_listar')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'editar_cliente.html', {'form': form, 'cliente': cliente})

def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('cliente_listar')
    return render(request, 'eliminar_cliente.html', {'cliente': cliente})

def membresiaAbm(request):
    contexto = {
        'membresias': Membresia.objects.all()
    }
    return render(request, 'membresiaAbm.html', contexto)

def crearMembresia(request):
    cliente_id = request.GET.get('cliente')
    cliente_obj = None
    if cliente_id:
        cliente_obj = get_object_or_404(Cliente, pk=cliente_id)

    if request.method == 'POST':
        form = membresiaForm(request.POST)
        if form.is_valid():
            memb = form.save(commit=False)
            if cliente_obj:
                memb.cliente = cliente_obj
            memb.save()
            return redirect('membresiaAbm')
    else:
        if cliente_obj:
            form = membresiaForm(initial={'cliente': cliente_obj.pk})
            if 'cliente' in form.fields:
                form.fields['cliente'].queryset = Cliente.objects.filter(pk=cliente_obj.pk)
                form.fields['cliente'].empty_label = None
        else:
            form = membresiaForm()

    return render(request, 'crearMembresia.html', {'form': form, 'cliente_obj': cliente_obj})

def elegir_cliente_para_membresia(request):
    clientes = Cliente.objects.select_related('usuario_id__user_id').all()
    return render(request, 'elegir_cliente.html', {'clientes': clientes})

def editarMembresia(request, pk):
    m = get_object_or_404(Membresia, pk=pk)
    queryset = Cliente.objects.filter(pk=m.cliente.id)
    if request.method == 'POST':
        membresia_Form = membresiaForm(request.POST, instance=m)
        membresia_Form.fields['cliente'].required = False
        membresia_Form.fields['cliente'].queryset = Cliente.objects.filter(pk=m.cliente.id)
        if membresia_Form.is_valid():
            mInst = membresia_Form.save(commit=False)
            mInst.cliente = m.cliente
            mInst.save()
            return redirect('membresiaAbm')
        else:
            print(membresia_Form.errors)
    else:
        membresia_Form = membresiaForm(instance=m)
        membresia_Form.fields['cliente'].required = False
        membresia_Form.fields['cliente'].queryset = queryset
        membresia_Form.fields['cliente'].initial = m.cliente
    contexto = {
        'user' : request.user,
        'membresiaForm': membresia_Form,
        'membresia': m
    }
    return render(request, 'editarMembresia.html', contexto)

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
