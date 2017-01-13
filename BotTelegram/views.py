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
        consulta = json.loads(request.body)
        logger.debug(consulta)
        atender_consulta_mensaje_tg(consulta)
    return HttpResponse('<h1>El Psy Congro</h1>')


@login_required
def mostrar_imagen(request,id_imagen):
    imagen = get_object_or_404(Imagen, pk=id_imagen)

    return render(request, 'imagen.html', {'imagen': imagen})


@login_required
def mostrar_imagenes(request):
    return render(request, 'imagenes.html', {'imagenes': Imagen.objects.all()})

@login_required
def webhook(request):

    contexto = {}
    if request.method == 'POST':
        form = FormEnviarMensaje(request.POST)
        if form.is_valid():
            print form.cleaned_data['mensaje']
            consulta = json.loads(form.cleaned_data['mensaje'])
            print type(consulta)
            logger.debug(consulta)
            atender_consulta_mensaje_tg(consulta)
    else:
        webhook_info = obtener_info_webhook()

        webhook_info = json.loads(webhook_info.text)

        if webhook_info:
            webhook_info = WebhookTG(webhook_info["result"])
            contexto["webhook"] = webhook_info

    return render(request,'webhook.html',contexto)

@login_required
def mostrar_me(request):
    contexto = {}
    me = obtener_info_me()

    me = json.loads(me.text)

    if me:
        me = UserTG(me["result"])
        contexto["bot"] = me

    return render(request,'me.html',contexto)

def home(request):
    return render(request,'home.html')


def pokemon(request):
    return render(request,'pokemon.html')

#'{"message": {"message_id": 150630,"from": {"id": 109518141, "username": "BREiViK", "last_name": "Koivula", "first_name": "Miika"},"photo": [{"width": 90, "height": 60, "file_id": "AgADBAADErwxG73W2AO1m_ZhTeVX7hvQnBkABCet0a09K0qs-6AAAgI","file_size": 1446},{"width": 131, "height": 87, "file_id": "AgADBAADErwxG73W2AO1m_ZhTeVX7hvQnBkABHsSTaJkXde8-qAAAgI","file_size": 3512}], "date": 1484298215,"chat": {"id": 109518141, "type": "private", "username": "BREiViK", "last_name": "Koivula","first_name": "Miika"}}, "update_id": 25289986}'