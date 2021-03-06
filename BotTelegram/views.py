# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from ClasesTG.user_tg import UserTG
from ClasesTG.webhook_tg import WebhookTG
from enviar_mensajes_usuario import *
from forms import FormEnviarMensaje
from maneja_respuesta import *

# Get an instance of a logger
logger = logging.getLogger("BotTelegram")


# Vista principal Home.
@login_required
def index(request):
    return render(request, 'base.html')


# Muestra una lista de los mensajes registrados enviados a la pagina
@login_required
def mostrar_mensajes(request):
    return render(request, 'mensajes.html', {'mensajes': []})


# Muestra todos los usuarios registrados
@login_required
def mostrar_usuarios(request):
    if request.method == "POST":  # Si se recive una peticion de enviar mensaje a todos
        form = FormEnviarMensaje(request.POST)
        if form.is_valid():
            enviar_mensaje_usuarios(form.cleaned_data['mensaje'])

    return render(request, 'usuarios.html', {'usuarios': Usuario.objects.all()})


# Muestra los datos de un usuario
@login_required
def mostrar_usuario(request, id_usuario):
    id_usuario = int(id_usuario)
    usuario_r = get_object_or_404(Usuario, pk=id_usuario)

    if request.method == "POST":
        form = FormEnviarMensaje(request.POST)
        if form.is_valid():
            enviar_mensaje_usuario(id_usuario, form.cleaned_data['mensaje'])

    return render(request, 'usuario.html', {'usuario': usuario_r})


# Recibe el mensaje(request de Telegram API) mandado por el usuario al bot y responde adecuadamente
@csrf_exempt
def atender_mensaje_usuario_tg(request):
    if request.method == 'POST':
        ## Convertimos el cuerpo del mensaje a un Json/Dict
        consulta = json.loads(request.body)
        ## Logeamos la consulta
        logger.debug(consulta)
        ## Llamamos a la función que va a atender el mensaje
        atender_consulta_mensaje_tg(consulta)

    # Telegram necesita una respuesta con http code 200
    return HttpResponse('<h1>El Psy Congro</h1>')


@login_required
def mostrar_imagen(request, id_imagen):
    imagen = get_object_or_404(Imagen, pk=id_imagen)

    return render(request, 'imagen.html', {'imagen': imagen})


@login_required
def mostrar_imagenes(request):
    return render(request, 'imagenes.html', {'imagenes': Imagen.objects.all()})


@login_required
def webhook(request):
    contexto = {}
    webhook_info = obtener_info_webhook()

    webhook_info = json.loads(webhook_info.text)

    if webhook_info:
        webhook_info = WebhookTG(webhook_info["result"])
        contexto["webhook"] = webhook_info

    if request.method == 'POST':
        form = FormEnviarMensaje(request.POST)
        if form.is_valid():
            consulta = json.loads(form.cleaned_data['mensaje'])
            atender_consulta_mensaje_tg(consulta)
            contexto["salida"] = "ok"

    return render(request, 'webhook.html', contexto)


@login_required
def mostrar_me(request):
    contexto = {}
    me = obtener_info_me()

    me = json.loads(me.text)

    if me:
        me = UserTG(me["result"])
        contexto["bot"] = me

    return render(request, 'me.html', contexto)


def home(request):
    return render(request, 'home.html')


def pokemon(request):
    return render(request, 'pokemon.html')
