from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from models import Usuario ,Mensaje,Imagen,ListaImagen,NodoImagen
import json
from maneja_respuesta import responder_usuario
from forms import LogPrincipalForm
import time


NOMBRE_USUARIO_MANUEL   = "manuggz"
PASSWORD_USUARIO_MANUEL = "Itadakimasu3093@!"
Logeado_manuel = False

# Create your views here.
def index(request):
	global Logeado_manuel
	if request.method == "POST":
		formUsuario = LogPrincipalForm(request.POST)
		if formUsuario.is_valid():
			if formUsuario.cleaned_data['username'] == NOMBRE_USUARIO_MANUEL and\
			   formUsuario.cleaned_data['username'] == NOMBRE_USUARIO_MANUEL:

				Logeado_manuel = True
				return render(request,'mensajes.html',{'mensajes':Mensaje.objects.all()})
		else:
			return render(request,'principal.html',{'form':LogPrincipalForm()})
	else:
		if Logeado_manuel:
			return render(request,'mensajes.html',{'mensajes':Mensaje.objects.all()})

		return render(request,'principal.html',{'form':LogPrincipalForm()})


def mostrarUsuario(request,id_usuario):
	if Logeado_manuel:
		id_usuario = int(id_usuario)
		usuario_r = Usuario.objects.get(pk=id_usuario)
		mensajes = Mensaje.objects.filter(usuario=usuario_r)

		return render(request,'usuario.html',{'usuario':usuario_r,
											  'total_ms_en':len(mensajes),
											  'mensajes':mensajes})	
	else:
		raise Http404()


@csrf_exempt
def responder_mensaje(request):

	if request.method == 'POST':
		time.sleep(1)
		consulta = json.loads(request.body)
		print consulta
		responder_usuario(consulta)
	else:
		raise Http404()
	return HttpResponse('OK')
