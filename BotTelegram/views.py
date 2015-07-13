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
		responder_usuario({u'update_id': 25205452, u'message': {u'text': u'/ \u0628\u0647\u062a\u0631\u06cc\u0646 \u0628\u0627\u0632\u06cc \u0648\u0627\u0644\u06cc\u0628\u0627\u0644 \u0627\u0646\u062f\u0631\u0648\u06cc\u062f\n\n\u06a9\u0627\u0645\u0644\u0627 \u0645\u062a\u0641\u0627\u0648\u062a \u0648 \u062e\u0644\u0627\u0642\u0627\u0646\u0647\U0001f44c\n\n\u0631\u0642\u0627\u0628\u062a \u062f\u0631 \u0642\u0627\u0644\u0628 \u0644\u06cc\u06af \u062c\u0647\u0627\u0646\u06cc \n\n\u0628\u0627 \u062d\u0636\u0648\u0631 \u062a\u06cc\u0645 \u0645\u0644\u06cc \u0627\u06cc\u0631\u0627\u0646 \u0648 \u062f\u06cc\u06af\u0631\u062a\u06cc\u0645 \u0647\u0627\u06cc \u0645\u0637\u0631\u062d \u062c\u0647\u0627\u0646\n\n\n\u0644\u06cc\u0646\u06a9 \u062f\u0627\u0646\u0644\u0648\u062f : \nhttp://uploadboy.com/ir8myvy1myfb.html\n\n\n\u067e\u06cc\u0634\u0646\u0647\u0627\u062f \u0645\u06cc\u06a9\u0646\u06cc\u0645 \u0628\u0647 \u0647\u06cc\u0686 \u0648\u062c\u0647 \u0627\u06cc\u0646 \u0628\u0627\u0632\u06cc \u0631\u0648 \u0627\u0632 \u062f\u0633\u062a \u0646\u062f\u0647\u06cc\u062f\U0001f44d\n\n\U0001f448\u062f\u0631 \u0636\u0645\u0646 \u0627\u06cc\u0646 \u0645\u0637\u0644\u0628 \u0631\u0648 \u0627\u0646\u062a\u0634\u0627\u0631 \u0628\u062f\u06cc\u062f \u062a\u0627 \u0647\u0645\u0647 \u0628\u062a\u0648\u0646\u0646 \u0627\u0632 \u0627\u06cc\u0646 \u0628\u0627\u0632\u06cc \u0644\u0630\u062a \u0628\u0628\u0631\u0646\U0001f449', u'chat': {u'title': u'Sexy bax', u'id': -10005425}, u'message_id': 6813, u'from': {u'first_name': u'Alireza.S', u'id': 96770304}, u'date': 1436808294}})
		raise Http404()
	return HttpResponse('OK')
