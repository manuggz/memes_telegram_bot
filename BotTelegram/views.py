from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from models import Usuario ,Mensaje,Imagen,ListaImagen,NodoImagen
import json
from maneja_respuesta import responder_usuario
from forms import LogPrincipalForm
import time


# NOMBRE_USUARIO_MANUEL   = "manuggz"
# PASSWORD_USUARIO_MANUEL = "Itadakimasu3093@!"
# Logeado_manuel = False

# Create your views here.
def index(request):
	return render(request,'base.html',{'form':LogPrincipalForm()})

def mostrarMensajes(request):
	return render(request,'mensajes.html',{'mensajes':Mensaje.objects.all()})

def mostrarUsuarios(request):
	return render(request,'usuarios.html',{'usuarios':Usuario.objects.all()})

def mostrarUsuario(request,id_usuario):
	id_usuario = int(id_usuario)
	usuario_r = Usuario.objects.get(pk=id_usuario)
	mensajes = Mensaje.objects.filter(usuario=usuario_r)

	return render(request,'usuario.html',{'usuario':usuario_r,
										  'total_ms_en':len(mensajes),
										  'mensajes':mensajes})	


@csrf_exempt
def responder_mensaje(request):

	if request.method == 'POST':
		time.sleep(1)
		consulta = json.loads(request.body)
		print consulta
		responder_usuario(consulta)
	else:
		responder_usuario({u'update_id': 25205664, u'message': {u'date': 1436813937, u'chat': {u'username': u'manuggz', u'first_name': u'Manuel', u'last_name': u'Gonzalez', u'id': 109518141}, u'from': {u'username': u'manuggz', u'first_name': u'Manuel', u'last_name': u'Gonzalez', u'id': 109518141}, u'message_id': 7541, u'text': u'/sendme forever alone ,Texto 1 - Texto 2 , blue'}})
		raise Http404()
	return HttpResponse('OK')
