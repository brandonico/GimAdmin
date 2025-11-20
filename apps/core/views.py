from django.shortcuts import render,redirect
#vista basada en clases
from django.views import View

#vista basada en funciones 
from django.http import HttpResponse
from django.http import JsonResponse

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

#idk
from django.core.exceptions import ObjectDoesNotExist

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
                
            else:
                try :
                    c = Cliente.objects.get(usuario=usuario)
                    entrada = timezone.now()
                    salida = entrada + timedelta(hours=2)
                    Asistencia.objects.create(cliente=c,
                                              hora_entrada=entrada,
                                              hora_salida=salida,
                                              capacidad=100)
                    #cambiar capacidad dependiendo
                except Cliente.DoesNotExist:
                    usuario = None

            if not usuario:
                contexto = {
                    'mensaje': 'El usuario no está registrado en la base.',
                    'cantidad': Asistencia.objects.count(),
                    'form' : form,
                }
                return render(request, 'home.html', contexto)
        
    contexto = {
        'form': form
    }
    return render(request, 'home.html', contexto)


def proteger_login(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

@proteger_login
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
        
    contexto = {}
    
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
            
            user.user_usuario.first_login = False
            user.user_usuario.save()

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
        try:
            membresia = usuario.user_usuario.cliente_usuario.membresia_cliente
            contexto['membresia'] = membresia
            cobranzas = Cobranza.objects.filter(membresia=membresia)
            contexto['cobranzas'] = list(cobranzas)
            if membresia.estado == 'Adeuda':
                nuevaCobranza = Cobranza(
                    membresia=membresia,
                    importe=settings.PRECIO_MES_SUSCRIPCION,
                    fecha_pago='A Decidir',
                    metodo_pago= 'A Decidir'
                    )
                setattr(nuevaCobranza, "a_pagar", "true")
                if nuevaCobranza:
                    contexto['cobranzas'].append(nuevaCobranza)

        except ObjectDoesNotExist:
            mensaje ='Cliente o Membresia no validas.'
            contexto = {
                'mensaje' : mensaje,
            }

            enviar_correo(
                asunto="Error - Login sin cliente/membresia",
                destinatario=settings.EMAIL_HOST_USER,
                contexto="Un usuario tiene problemas para iniciar sesion por no figurar en las listas de clientes o membresia.\n"
                "\nApellido y Nombre: " + usuario.last_name + " " + usuario.first_name + 
                "\nEmail: " + usuario.email + 
                "\nDNI: " + str(usuario.user_usuario.dni),
                plantilla_html=""
            )
            
            logout(request)
            return render(request, 'login.html', contexto)

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
    if request.method == "POST":
        form = ActualizarMembresiaForm(request.POST)
        if form.is_valid():
            membresia.fecha_inicio = form.cleaned_data['fecha_inicio']
            membresia.fecha_fin = form.cleaned_data['fecha_fin']
            membresia.estado = form.cleaned_data['estado']
            membresia.save()

            cobranza = Cobranza.objects.create( membresia=membresia,
                                                importe=form.cleaned_data['importe'],
                                                metodo_pago=form.cleaned_data['metodo_pago']
                                                )
            cuerpo= "Usted ha abonado otro plazo con Oxigeno: \nPlazo: "+membresia.fecha_inicio.strftime("%d/%m/%Y") +" a "+ membresia.fecha_fin.strftime("%d/%m/%Y")+"\nImporte: $"+str(cobranza.importe)+"\nMetodo de pago: "+cobranza.metodo_pago
            enviar_correo(
                asunto="Muchas Gracias",
                destinatario=membresia.cliente.usuario.user.email,
                contexto=cuerpo,
                plantilla_html=""
            )
            return redirect('dashboard')
            
    return render (request, 'actualizar_membresia.html', contexto)

@staff_member_required(login_url='/permisos_insuficientes/')
def baja_membresia (request, pk):
    membresia = Membresia.objects.get(id=pk)
    membresia.estado='Baja'
    membresia.save()
    return redirect('dashboard')

def actualizar_asistencia (request):
    cuenta = Asistencia.objects.filter(
            fecha_clase=timezone.localtime().date(),
            hora_salida__gt= timezone.localtime().time()
            ).count()       #Filtra las ultimas 2 horas de asistencias
                            #tiene en cuenta fecha y hora. __gt = mayor que
    if (cuenta <= settings.LIMITE_ASISTENCIA_MEDIO):
        color = '#22bb33';
    elif (cuenta <= settings.LIMITE_ASISTENCIA_ALTO):
        color = '#f0ad4e';
    else:
        color = '#bb2124'
    
    datos = {
        'cantidad': cuenta,
        'color' : color
    }                   

    return JsonResponse(datos)

def crear_asistencia(request):
    dni = request.GET.get("dni", "")

    try :
        usuario = UserProfile.objects.get(dni=dni)
    except UserProfile.DoesNotExist:
        usuario = None
        
    try :
        c = Cliente.objects.get(usuario=usuario)
        entrada = timezone.now()
        salida = entrada + timedelta(hours=2)
        Asistencia.objects.create(cliente=c,
                                    hora_entrada=entrada,
                                    hora_salida=salida,
                                    capacidad=100)
        #cambiar capacidad dependiendo
    except Cliente.DoesNotExist:
        c = None

    contexto = {"mensaje":""}

    if not usuario:
        contexto = {
            'mensaje': 'El usuario no está registrado en la base.',
        }
    elif not c:
        contexto = {
            'mensaje':'El usuario no es un cliente registrado'
        }
    return JsonResponse(contexto)