from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from models import Usuario ,Mensaje,Imagen,ListaImagen,NodoImagen
import json
from maneja_respuesta import responder_usuario,enviarMensajeTexto,enviarMensajeATodosUsuarios
from forms import LogPrincipalForm,FormEnviarMensaje
import time


# NOMBRE_USUARIO_MANUEL   = "manuggz"
# PASSWORD_USUARIO_MANUEL = "Itadakimasu3093@!"
# Logeado_manuel = False

# Create your views here.
def index(request):
	return render(request,'base.html')

def mostrarMensajes(request):
	return render(request,'mensajes.html',{'mensajes':Mensaje.objects.all()})

def mostrarUsuarios(request):

	if request.method == "POST":
		form = FormEnviarMensaje(request.POST)
		if form.is_valid():
			enviarMensajeATodosUsuarios(form.cleaned_data['mensaje'])

	return render(request,'usuarios.html',{'usuarios':Usuario.objects.all()})

def mostrarUsuario(request,id_usuario):
	id_usuario = int(id_usuario)
	usuario_r = get_object_or_404(Usuario, pk=id_usuario) 
	mensajes = Mensaje.objects.filter(usuario=usuario_r)

	if request.method == "POST":
		form = FormEnviarMensaje(request.POST)
		if form.is_valid():
			enviarMensajeTexto(id_usuario,form.cleaned_data['mensaje'])

                  
	return render(request,'usuario.html',{'usuario':usuario_r,'total_ms_en':len(mensajes),
										  'mensajes':mensajes})	


@csrf_exempt
def responder_mensaje(request):

	if request.method == 'POST':
		time.sleep(1)
		consulta = json.loads(request.body)
		print consulta
		responder_usuario(consulta)
	else:
		# mensaje = u"/help sendme"
		# chid = 12500
		# upid = 25208203
		# responder_usuario({u'message': {u'chat': {u'first_name': u'Manuel', u'id': 109518141, u'username': u'manuggz', u'last_name': u'Gonzalez'}, u'text': mensaje, u'from': {u'first_name': u'Manuel', u'id': 109518141, u'username': u'manuggz', u'last_name': u'Gonzalez'}, u'date': 1437074942, 
		# 	u'message_id': chid}, u'update_id': upid})
		return redirect('/BotTelegram/')
	return HttpResponse('OK')
