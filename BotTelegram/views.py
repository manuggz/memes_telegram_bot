from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from maneja_respuesta import *
from forms import FormEnviarMensaje
import time


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
        #time.sleep(1)  # Para no saturar al servidor
        consulta = json.loads(request.body)
        print consulta
        atender_consulta_mensaje_tg(consulta)
    else:
        mensaje = u"/random"
        chid = 109518141
        upid = 25208203
        atender_consulta_mensaje_tg({u'message': {u'text': mensaje,
                                                  u'from': {u'first_name': u'SaDeGh', u'id': chid,
                                                            u'username': u'Saditurboo'},
                                                  u'chat': {u'first_name': u'SaDeGh', u'id': chid,
                                                            u'username': u'Saditurboo', u'type': u'private'},
                                                  u'message_id': 905476, u'date': 1475391962}, u'update_id': 25256647})
    # return redirect('/BotTelegram/')
    return HttpResponse('OK')
