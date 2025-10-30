from django.shortcuts import render, redirect, get_object_or_404

from .models import UserProfile, Cliente, Membresia, Asistencia, Cobranza
from django.contrib.auth.models import User

from .forms import UsuarioForm, UserForm, ClienteForm, MembresiaForm, AsistenciaForm, CobranzaForm
import random, string

def lista_usuarios(request):
    contexto = {
        'user' : request.user,
        'usuarios': UserProfile.objects.all()
    }
    return render(request, 'lista_usuarios.html', contexto)

def generar_contraseña_temporal(longitud=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=longitud))

def crear_usuario(request):
    if request.method == 'POST':
        user_Form = UserForm(request.POST)
        usuario_Form = UsuarioForm(request.POST)
        if user_Form.is_valid() and usuario_Form.is_valid():
            u = User.objects.create_user(
                username = user_Form.cleaned_data['email'],
                password = generar_contraseña_temporal(),
                email = user_Form.cleaned_data['email'],
                first_name = user_Form.cleaned_data['first_name'],
                last_name = user_Form.cleaned_data['last_name'],
                is_superuser = user_Form.cleaned_data['is_superuser'],
                is_staff = user_Form.cleaned_data['is_staff']
            )
            uPerfil = UserProfile.objects.create(
                user = u,
                dni = usuario_Form.cleaned_data['dni'],
                telefono = usuario_Form.cleaned_data['telefono'],
                domicilio = usuario_Form.cleaned_data['domicilio'],
                fecha_nac = usuario_Form.cleaned_data['fecha_nac']
            )
            u.save()
            uPerfil.save()
            return redirect('usuario_listar')
    else:
        user_Form = UserForm()
        usuario_Form = UsuarioForm()
    
    contexto = {
        'user' : request.user,
        'usuarioForm': usuario_Form,
        'userForm': user_Form,
    }
    return render(request, 'crear_usuario.html', contexto)

def editar_usuario(request, pk):
    u = get_object_or_404(User, pk=pk)
    uPerfil = get_object_or_404(UserProfile, user_id=pk)
    if request.method == 'POST':    
        user_Form = UserForm(request.POST, instance=u)
        usuario_Form = UsuarioForm(request.POST, instance=uPerfil)
        if user_Form.is_valid() and usuario_Form.is_valid():
            u = user_Form.save(commit=False)
            u.username = u.email
            uPerfil = usuario_Form.save(commit=False)
            u.save()
            uPerfil.save()
            return redirect('usuario_listar')
    else:
        user_Form = UserForm(instance=u)
        usuario_Form = UsuarioForm(instance=uPerfil)
    contexto = {
        'user' : request.user,
        'usuarioForm': usuario_Form,
        'userForm': user_Form,
        'es_edicion': True
    }
    return render(request, 'crear_usuario.html', contexto)

def eliminar_usuario(request, pk):
    print(pk)
    u = get_object_or_404(User, pk=pk)
    u.delete()
    return redirect('usuario_listar')

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'lista_clientes.html', {'clientes': clientes})

def crear_cliente(request, user_id):
    perfil = get_object_or_404(UserProfile, pk=user_id)

    if Cliente.objects.filter(usuario_id=perfil).exists():
        return redirect('cliente_listar')

    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario = perfil
            cliente.save()
            return redirect('cliente_listar')
    else:
        form = ClienteForm()
    return render(request, 'crear_cliente.html', {'ClienteForm': form, 'perfil': perfil})

def elegir_usuario_para_cliente(request):
    ids_usados = Cliente.objects.values_list('usuario', flat=True)
    perfiles = UserProfile.objects.exclude(id__in=ids_usados)

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
    perfil = cliente.usuario
    return render(request, 'crear_cliente.html', {'ClienteForm': form, 'cliente': cliente, 'es_edicion': True, 'perfil': perfil})

def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('cliente_listar')
    return render(request, 'eliminar_cliente.html', {'cliente': cliente})

def lista_membresias(request):
    contexto = {
        'membresias': Membresia.objects.all()
    }
    return render(request, 'lista_membresias.html', contexto)

def crear_membresia(request, cliente):
    cliente_obj = get_object_or_404(Cliente, id=cliente)

    if request.method == 'POST':
        form = MembresiaForm(request.POST)
        if form.is_valid():
            memb = form.save(commit=False)
            if cliente_obj:
                memb.cliente = cliente_obj
            memb.save()
            return redirect('lista_membresias')
    else:
        if cliente_obj:
            form = MembresiaForm(initial={'cliente': cliente_obj.pk})
            if 'cliente' in form.fields:
                form.fields['cliente'].queryset = Cliente.objects.filter(pk=cliente_obj.pk)
                form.fields['cliente'].empty_label = None
        else:
            form = MembresiaForm()

    return render(request, 'crear_membresia.html', {'membresiaForm': form, 'cliente_obj': cliente_obj})

def elegir_cliente_para_membresia(request):
    ids_usados = Membresia.objects.values_list('cliente', flat=True)
    clientes = Cliente.objects.exclude(id__in=ids_usados)
    return render(request, 'elegir_cliente.html', {'clientes': clientes})

def editar_membresia(request, pk):
    m = get_object_or_404(Membresia, pk=pk)
    queryset = Cliente.objects.filter(pk=m.cliente.id)
    if request.method == 'POST':
        membresia_Form = MembresiaForm(request.POST, instance=m)
        membresia_Form.fields['cliente'].required = False
        membresia_Form.fields['cliente'].queryset = Cliente.objects.filter(pk=m.cliente.id)
        if membresia_Form.is_valid():
            mInst = membresia_Form.save(commit=False)
            mInst.cliente = m.cliente
            mInst.save()
            return redirect('lista_membresias')
        else:
            print(membresia_Form.errors)
    else:
        membresia_Form = MembresiaForm(instance=m)
        membresia_Form.fields['cliente'].required = False
        membresia_Form.fields['cliente'].queryset = queryset
        membresia_Form.fields['cliente'].initial = m.cliente
    contexto = {
        'user' : request.user,
        'membresiaForm': membresia_Form,
        'membresia': m,
    }
    return render(request, 'editarMembresia.html', contexto)

def eliminar_membresia(request, pk):
    m = get_object_or_404(Membresia, pk=pk)
    m.delete()
    return redirect('lista_membresias')

def lista_asistencias(request):
    contexto = {
        'asistencias': Asistencia.objects.all()
    }
    return render(request, 'lista_asistencias.html', contexto)

def elegir_cliente_para_asistencia(request):
    clientes= Cliente.objects.get().all()
    return render(request, 'elegir_cobranza.html', {'clientes': clientes})

def crear_asistencia(request):
    if request.method == 'POST':
        asistencia_Form = AsistenciaForm(request.POST)
        if asistencia_Form.is_valid():
            asistencia_Form.save()
            return redirect('lista_asistencias')
        else:
            print(asistencia_Form.errors)
    else:
        asistencia_Form = AsistenciaForm()
    contexto = {
        'user' : request.user,
        'asistenciaForm': asistencia_Form,
    }
    return render(request, 'crear_asistencia.html', contexto)

def editar_asistencia(request, pk):
    a = get_object_or_404(Asistencia, pk=pk)
    if request.method == 'POST':
        asistencia_Form = AsistenciaForm(request.POST, instance=a)
        if asistencia_Form.is_valid():
            asistencia_Form.save()
            return redirect('lista_asistencias')
        else:
            print(asistencia_Form.errors)
    else:
        asistencia_Form = AsistenciaForm(instance=a)
    contexto = {
        'user' : request.user,
        'asistenciaForm': asistencia_Form,
        'asistencia': a
    }
    return render(request, 'editarAsistencia.html', contexto)

def eliminar_asistencia(request, pk):
    a = get_object_or_404(Asistencia, pk=pk)
    a.delete()
    return redirect('lista_asistencias')

def lista_cobranzas(request):
    contexto = {
        'cobranzas': Cobranza.objects.all()
    }
    return render(request, 'lista_cobranzas.html', contexto)

def elegir_membresia_para_cobranza(request):
    membresias = Membresia.objects.get().all()
    return render(request, 'elegir_cobranza.html', {'membresias': membresias})


def crear_cobranza(request):
    if request.method == 'POST':
        cobranza_Form = CobranzaForm(request.POST)
        if cobranza_Form.is_valid():
            cobranza_Form.save()
            return redirect('lista_cobranzas')
        else:
            print(cobranza_Form.errors)
    else:
        cobranza_Form = CobranzaForm()
    contexto = {
        'user' : request.user,
        'cobranzaForm': cobranza_Form,
    }
    return render(request, 'crear_cobranza.html', contexto)

def editar_cobranza(request, pk):
    c = get_object_or_404(Cobranza, pk=pk)
    if request.method == 'POST':
        cobranza_Form = CobranzaForm(request.POST, instance=c)
        if cobranza_Form.is_valid():
            cobranza_Form.save()
            return redirect('lista_cobranzas')
        else:
            print(cobranza_Form.errors)
    else:
        cobranza_Form = CobranzaForm(instance=c)
    contexto = {
        'user' : request.user,
        'cobranzaForm': cobranza_Form,
        'cobranza': c,
        'es_edicion' : True
    }
    return render(request, 'crear_cobranza.html', contexto)

def eliminar_cobranza(request, pk):
    a = get_object_or_404(Cobranza, pk=pk)
    a.delete()
    return redirect('lista_cobranzas')
