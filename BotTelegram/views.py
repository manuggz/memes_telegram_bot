from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from enviar_mensajes_usuario import *
from maneja_respuesta import *
from forms import FormEnviarMensaje


# Vista principal Home.
def index(request):
    return render(request, 'base.html')


# Muestra una lista de los mensajes registrados enviados a la pagina
def mostrar_mensajes(request):
    return render(request, 'mensajes.html', {'mensajes': RespuestaServidor.objects.all()})


# Muestra todos los usuarios registrados
def mostrar_usuarios(request):
    if request.method == "POST":  # Si se recive una peticion de enviar mensaje a todos
        form = FormEnviarMensaje(request.POST)
        if form.is_valid():
            enviar_mensaje_usuarios(form.cleaned_data['mensaje'])

    return render(request, 'usuarios.html', {'usuarios': Usuario.objects.all()})


# Muestra los datos de un usuario
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
        pass
        #mensaje = u"/start"
        #chid = 109518141
        #upid = 25208203
        #atender_consulta_mensaje_tg({u'callback_query': {u'id': u'470376834666675591', u'from': {u'id': 109518141, u'username': u'manuggz', u'first_name': u'Manuel', u'last_name': u'Gonzalez'}, u'data': u'random', u'chat_instance': u'-3266157052870893227', u'message': {u'date': 1475880556, u'chat': {u'id': 109518141, u'username': u'manuggz', u'first_name': u'Manuel', u'last_name': u'Gonzalez', u'type': u'private'}, u'message_id': 107957, u'photo': [{u'width': 77, u'file_size': 2133, u'height': 90, u'file_id': u'AgADAQADbgIyG3unIQf_AAH8zJ8PNjbHrOcvAAQITUDiZyMGg-GtAQABAg'}, {u'width': 208, u'file_size': 10772, u'height': 242, u'file_id': u'AgADAQADbgIyG3unIQf_AAH8zJ8PNjbHrOcvAARgzOu37xIOzOCtAQABAg'}], u'from': {u'id': 119646075, u'username': u'MemesBot', u'first_name': u'Memes'}, u'caption': u'forever alone'}}, u'update_id': 25257748})

        # atender_consulta_mensaje_tg({u'update_id': 25257467, u'callback_query': {u'data': u'random', u'message': {u'photo': [
        # {u'file_id': u'AgADAQADnwEyG3unIQeHf8_1SA8rG42t5y8ABPFY1bJSpotw-akBAAEC', u'height': 90, u'file_size': 2033,
        #  u'width': 71},
        # {u'file_id': u'AgADAQADnwEyG3unIQeHf8_1SA8rG42t5y8ABGL1XRgTI1nU-qkBAAEC', u'height': 320, u'file_size': 25701,
        #  u'width': 254},
        # {u'file_id': u'AgADAQADnwEyG3unIQeHf8_1SA8rG42t5y8ABPvOMuFw8amT-KkBAAEC', u'height': 425, u'file_size': 27222,
        #  u'width': 337}], u'chat': {u'last_name': u'Gonzalez', u'type': u'private', u'first_name': u'Manuel',
        #                             u'id': 109518141, u'username': u'manuggz'}, u'from': {u'first_name': u'Memes',
        #                                                                                   u'id': 119646075,
        #                                                                                   u'username': u'MemesBot'},
        #                                                                           u'date': 1475790308,
        #                                                                           u'caption': u'Chuck Norris',
        #                                                                           u'message_id': 107203},
        #                                          u'chat_instance': u'-3266157052870893227',
        #                                          u'id': u'470376835400986871',
        #                                          u'from': {u'last_name': u'Gonzalez', u'first_name': u'Manuel',
        #                                                    u'id': 109518141, u'username': u'manuggz'}},"debug":True})


    return HttpResponse('OK')


def mostrar_imagen(request,id_imagen):
    id_usuario = int(id_imagen)
    imagen = get_object_or_404(Imagen, pk=id_imagen)

    return render(request, 'imagen.html', {'imagen': imagen})


def mostrar_imagenes(request):
    return render(request, 'imagenes.html', {'imagenes': Imagen.objects.all()})
