from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from BotTelegram.user_tg import UserTG
from BotTelegram.webhook_tg import WebhookTG
from enviar_mensajes_usuario import *
from maneja_respuesta import *
from forms import FormEnviarMensaje


# Vista principal Home.
@login_required
def index(request):
    return render(request, 'base.html')


# Muestra una lista de los mensajes registrados enviados a la pagina
@login_required
def mostrar_mensajes(request):
    return render(request, 'mensajes.html', {'mensajes': RespuestaServidor.objects.all()})


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
    mensajes = RespuestaServidor.objects.filter(usuario=usuario_r)

    if request.method == "POST":
        form = FormEnviarMensaje(request.POST)
        if form.is_valid():
            enviar_mensaje_usuario(id_usuario, form.cleaned_data['mensaje'])

    return render(request, 'usuario.html', {'usuario': usuario_r, 'total_ms_en': len(mensajes), 'mensajes': mensajes})


# Recibe el mensaje(request de Telegram API) mandado por el usuario al bot y responde adecuadamente
@csrf_exempt
def atender_mensaje_usuario_tg(request):
    if request.method == 'POST':
        consulta = json.loads(request.body)
        print consulta
        atender_consulta_mensaje_tg(consulta)
    else:
        mensaje = u"LOL"
        chid = 109518141
        upid = 25208203
        atender_consulta_mensaje_tg({u'update_id': 25257960, u'message': {u'message_id': 108263, u'date': 1475969549, u'entities': [{u'type': u'bot_command', u'offset': 0, u'length': 7}], u'chat': {u'username': u'manuggz', u'type': u'private', u'first_name': u'Manuel', u'last_name': u'Gonzalez', u'id': 109518141}, u'from': {u'username': u'manuggz', u'first_name': u'Manuel', u'last_name': u'Gonzalez', u'id': 109518141}, u'text': mensaje}})

        #random
        #atender_consulta_mensaje_tg({u'callback_query': {u'message': {u'from': {u'id': 119646075, u'first_name': u'Memes', u'username': u'MemesBot'}, u'date': 1476129023, u'caption': u'boobs_quote', u'message_id': 109060, u'chat': {u'id': 109518141, u'type': u'private', u'last_name': u'Gonzalez', u'first_name': u'Manuel', u'username': u'manuggz'}, u'photo': [{u'height': 90, u'width': 63, u'file_size': 1661, u'file_id': u'AgADAQADxAQyG3unIQc4XhXB1owN7QaZ5y8ABORpkD9zj8V14rMBAAEC'}, {u'height': 320, u'width': 224, u'file_size': 21166, u'file_id': u'AgADAQADxAQyG3unIQc4XhXB1owN7QaZ5y8ABEFMdcOyWVIL47MBAAEC'}, {u'height': 800, u'width': 559, u'file_size': 85369, u'file_id': u'AgADAQADxAQyG3unIQc4XhXB1owN7QaZ5y8ABN-X0engzx9q5LMBAAEC'}, {u'height': 801, u'width': 560, u'file_size': 79950, u'file_id': u'AgADAQADxAQyG3unIQc4XhXB1owN7QaZ5y8ABEiNMZ4ZYAABuuGzAQABAg'}]}, u'id': u'470376835817714395', u'from': {u'id': 109518141, u'last_name': u'Gonzalez', u'first_name': u'Manuel', u'username': u'manuggz'}, u'chat_instance': u'-3266157052870893227', u'data': u'Random'}, u'update_id': 25258566})

        #next
        #atender_consulta_mensaje_tg({u'callback_query': {u'message': {u'from': {u'id': 119646075, u'first_name': u'Memes', u'username': u'MemesBot'}, u'date': 1476129193, u'caption': u'Yao Ming LOL', u'message_id': 109062, u'chat': {u'id': 109518141, u'type': u'private', u'last_name': u'Gonzalez', u'first_name': u'Manuel', u'username': u'manuggz'}, u'photo': [{u'height': 90, u'width': 77, u'file_size': 1857, u'file_id': u'AgADAQADxgQyG3unIQfYweWz-QkxjRCB5y8ABK5ohjQzZbA4lLEBAAEC'}, {u'height': 320, u'width': 273, u'file_size': 16348, u'file_id': u'AgADAQADxgQyG3unIQfYweWz-QkxjRCB5y8ABMIYd0jIX2KclbEBAAEC'}, {u'height': 586, u'width': 500, u'file_size': 27963, u'file_id': u'AgADAQADxgQyG3unIQfYweWz-QkxjRCB5y8ABC0XwiR4op2Qk7EBAAEC'}]}, u'id': u'470376835093914980', u'from': {u'id': 109518141, u'last_name': u'Gonzalez', u'first_name': u'Manuel', u'username': u'manuggz'}, u'chat_instance': u'-3266157052870893227', u'data': u'SetUpperText'}, u'update_id': 25258567})

    return HttpResponse('OK')


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


