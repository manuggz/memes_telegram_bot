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
    #atender_consulta_mensaje_tg({u'message': {u'from': {u'id': 109518141, u'last_name': u'Gonzalez', u'first_name': u'Manuel', u'username': u'manuggz'}, u'message_id': 125451, u'date': 1478470319, u'photo': [{u'width': 67, u'file_size': 1208, u'height': 90, u'file_id': u'AgADAQADw6gxGz0dhwa2w-3ZhfsiJB6b5y8ABE1iGixSkTr17fgBAAEC'}, {u'width': 240, u'file_size': 12470, u'height': 320, u'file_id': u'AgADAQADw6gxGz0dhwa2w-3ZhfsiJB6b5y8ABH7AejmJ2cLc7vgBAAEC'}, {u'width': 599, u'file_size': 54354, u'height': 800, u'file_id': u'AgADAQADw6gxGz0dhwa2w-3ZhfsiJB6b5y8ABNK-nmEbCuXS7_gBAAEC'}, {u'width': 959, u'file_size': 83277, u'height': 1280, u'file_id': u'AgADAQADw6gxGz0dhwa2w-3ZhfsiJB6b5y8ABJu_Dvb5mYGK7PgBAAEC'}], u'chat': {u'id': 109518141, u'last_name': u'Gonzalez', u'first_name': u'Manuel', u'type': u'private', u'username': u'manuggz'}}, u'update_id': 25269293})
    # atender_consulta_mensaje_tg({u'callback_query': {u'id': u'470376834131679783',
    #                      u'from': {u'id': 109518141, u'last_name': u'Gonzalez', u'first_name': u'Manuel',
    #                                u'username': u'manuggz'}, u'chat_instance': u'-3266157052870893227',
    #                      u'data': u'SetUpperText,',
    #                      u'message': {u'from': {u'id': 119646075, u'username': u'MemesBot', u'first_name': u'Memes'},
    #                                   u'message_id': 125453, u'date': 1478470792, u'photo': [
    #                              {u'width': 67, u'file_size': 1588, u'height': 90,
    #                               u'file_id': u'AgADAQADVyIyG3unIQecW7TbIrkOtaGa5y8ABDZ4Plpn22TzfvgBAAEC'},
    #                              {u'width': 240, u'file_size': 17742, u'height': 320,
    #                               u'file_id': u'AgADAQADVyIyG3unIQecW7TbIrkOtaGa5y8ABH7Ja0CQhoqDf_gBAAEC'},
    #                              {u'width': 599, u'file_size': 68672, u'height': 800,
    #                               u'file_id': u'AgADAQADVyIyG3unIQecW7TbIrkOtaGa5y8ABOLAfaxTBQr1ffgBAAEC'},
    #                              {u'width': 959, u'file_size': 119937, u'height': 1280,
    #                               u'file_id': u'AgADAQADVyIyG3unIQecW7TbIrkOtaGa5y8ABB1bncBum7L8fPgBAAEC'}],
    #                                   u'chat': {u'id': 109518141, u'last_name': u'Gonzalez', u'first_name': u'Manuel',
    #                                             u'type': u'private', u'username': u'manuggz'}}}, u'update_id': 25269294})
    #atender_consulta_mensaje_tg({u'message': {u'text': u'yo upper!', u'from': {u'id': 109518141, u'last_name': u'Gonzalez', u'first_name': u'Manuel', u'username': u'manuggz'}, u'message_id': 125456, u'date': 1478471058, u'chat': {u'id': 109518141, u'last_name': u'Gonzalez', u'first_name': u'Manuel', u'type': u'private', u'username': u'manuggz'}}, u'update_id': 25269295})
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


