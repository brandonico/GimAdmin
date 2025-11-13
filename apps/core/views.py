from django.shortcuts import render,redirect
#vista basada en clases
from django.views import View

#vista basada en funciones 
from django.http import HttpResponse

#importar authenticate
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

#importar modelos
from .forms import CrearAsistenciaForm, ActualizarMembresiaForm
from apps.abm.models import Cliente, UserProfile, Asistencia, Membresia, Cobranza

#importar tiempo para asistencia
from django.utils import timezone
from datetime import timedelta

#importa correo
from apps.core.utils import enviar_correo
from django.contrib.auth.models import User
import random, string

#importar conf
from django.conf import settings

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
        'cantidad': Asistencia.objects.count(),#Filtrar las ultimas 2 horas de asistencias
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
            
            profile = UserProfile.objects.get(user=user)
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
            logout(request)
            return redirect('login')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')

    return render(request, 'first_login.html')

@login_required
def logoutView(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    nuevaCobranza = None
    usuario = request.user
    contexto = {
        'user' : usuario,
    }
    if usuario.is_staff:
        miembrosAdeudados = list(Membresia.objects.filter(estado='Adeuda'))
        cobranzas = []
        for miembro in miembrosAdeudados:
            nuevaCobranza = Cobranza(
                membresia=miembro,
                importe=settings.PRECIO_MES_SUSCRIPCION,
                fecha_pago='A Decidir',
                metodo_pago='A decidir'
                )
            setattr(nuevaCobranza, "a_pagar", "true")
            cobranzas.append(nuevaCobranza)
        contexto['cobranzas'] = cobranzas
        return render (request, 'dashboard.html', contexto)
    else:
        membresia = usuario.user_usuario.cliente_usuario.membresia_cliente
        contexto['membresia'] = membresia
        cobranzas = Cobranza.objects.filter(membresia=membresia)
        contexto['cobranzas'] = list(cobranzas)
        if membresia.estado == 'Adeuda':
            nuevaCobranza = Cobranza(
                membresia=membresia,
                importe=settings.PRECIO_MES_SUSCRIPCION,
                fecha_pago='A Decidir',
                metodo_pago= 'A decidir'
                )
            setattr(nuevaCobranza, "a_pagar", "true")
            if nuevaCobranza:
                contexto['cobranzas'].append(nuevaCobranza)
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

def permisos_insuficientes(request):
    return render(request, "permisos_insuficientes.html", {"mensaje" : 'mensaje'})

@staff_member_required(login_url='/permisos_insuficientes/')
def actualizar_membresia (request, pk):
    form = ActualizarMembresiaForm()
    membresia = Membresia.objects.get(id=pk)
    contexto = {
        'form' : form,
        'membresia': membresia,
    }



    render (request, 'actualizar_membresia.html', contexto)
    pass

@staff_member_required(login_url='/permisos_insuficientes/')
def baja_membresia (request, pk):
    membresia = Membresia.objects.get(id=pk)
    membresia.estado='Baja'
    membresia.save
    return redirect('dashboard')