from django.shortcuts import render,redirect,get_object_or_404

from .models import userProfile, Cliente, Membresia, Asistencia
from django.contrib.auth.models import User

from .forms import usuarioForm, userForm, clienteForm, membresiaForm
from .forms import ClienteForm

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

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'lista_clientes.html', {'clientes': clientes})

def crear_cliente(request, user_id):
    perfil = get_object_or_404(userProfile, pk=user_id)

    if Cliente.objects.filter(usuario_id=perfil).exists():
        return redirect('cliente_listar')

    if request.method == 'POST':
        form = ClienteForm(request.POST)
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
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'editar_cliente.html', {'form': form, 'cliente': cliente})

def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')
    return render(request, 'eliminar_cliente.html', {'cliente': cliente})

def membresiaAbm(request):
    contexto = {
        'membresias': Membresia.objects.all()
    }
    return render(request, 'membresiaAbm.html', contexto)

def crearMembresia(request):
    if request.method == 'POST':
        membresia_Form = membresiaForm(request.POST)
        if membresia_Form.is_valid():
            m = Membresia.objects.create(
                cliente = membresia_Form.cleaned_data['cliente'],
                fecha_inicio = membresia_Form.cleaned_data['fecha_inicio'],
                fecha_fin = membresia_Form.cleaned_data['fecha_fin'],
                importe = membresia_Form.cleaned_data['importe'],
                estado = membresia_Form.cleaned_data['estado']
            )
            m.save()
            return redirect('membresiaAbm')
    else:
        membresia_Form = membresiaForm()
        membresiaInstancia = Membresia.objects.get()
        contexto = {
            'user' : request.user,
            'membresiaForm': membresia_Form,
            'membresia' : membresiaInstancia
        }
    return render(request, 'crearMembresia.html', contexto)

def editarMembresia(request, pk):
    if request.method == 'POST':
        membresia_Form = membresiaForm(request.POST)
        if membresia_Form.is_valid():
            m = get_object_or_404(Membresia, pk=pk)

            m.fecha_inicio = membresia_Form.cleaned_data['fecha_inicio']
            m.fecha_fin = membresia_Form.cleaned_data['fecha_fin']
            m.importe = membresia_Form.cleaned_data['importe']
            m.estado = membresia_Form.cleaned_data['estado']
            m.save()
            return redirect('membresiaAbm')
            
    else:
        membresiaInstancia = get_object_or_404(Membresia, pk=pk)
        membresia_Form = membresiaForm(instance=membresiaInstancia)
    contexto = {
        'user' : request.user,
        'membresiaForm': membresia_Form,
        'membresia': membresiaInstancia
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
