from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def enviar_correo(asunto, destinatario, contexto, plantilla_html=None):
    """
    Envía correos con soporte para versión HTML
    Args:
        asunto: Título del correo
        destinatarios: Lista de direcciones email
        texto: Contenido en texto plano
        html: Contenido HTML opcional
    """
    print(asunto)
    print(destinatario)
    print(contexto)
    print(plantilla_html)

    email = EmailMultiAlternatives(
        subject=asunto,
        body=contexto,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[destinatario]
    )

    if plantilla_html:
        email.attach_alternative(plantilla_html, 'text/html')

    email.send()
    return True

def recibir_correo(remitente, asunto, contexto, plantilla_html=None):
    """
    para recibir los correos de la gente en home
    Args:
        remitente: Dirección email del remitente
        asunto: Título del correo
        contexto: Contenido en texto plano
        html: Contenido HTML opcional
    """
    print(remitente)
    print(asunto)
    print(contexto)
    print(plantilla_html)

    email = EmailMultiAlternatives(
        subject=asunto,
        body=contexto,
        from_email=remitente,
        to=[settings.DEFAULT_FROM_EMAIL],
    )

    if plantilla_html:
        email.attach_alternative(plantilla_html, 'text/html')

    email.send()
    return True