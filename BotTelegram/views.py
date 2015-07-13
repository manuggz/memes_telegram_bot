from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from models import Usuario ,Mensaje,Imagen,ListaImagen,NodoImagen
import json
from maneja_respuesta import responder_usuario



# Create your views here.
def index(request):
	return render(request,'index.html',{'mensajes':Mensaje.objects.all()})

def mostrarUsuario(request,id_usuario):
	id_usuario = int(id_usuario)
	return render(request,'usuario.html',{'usuario':Usuario.objects.get(pk=id_usuario)})	

@csrf_exempt
def responder_mensaje(request):

	if request.method == 'POST':
		consulta = json.loads(request.body)
		print consulta
		responder_usuario(consulta)
	else:
		#responder_usuario({u'update_id': 25204849, u'message': {u'chat': {u'id': 30892118, u'first_name': u'Jacopo', u'last_name': u'\U0001f3b8', u'username': u'Jacknot'}, u'from': {u'id': 30892118, u'first_name': u'Jacopo', u'last_name': u'\U0001f3b8', u'username': u'Jacknot'}, u'message_id': 5167,u'date': 1436799388, u'text': u'/sendme trollface, lol, white'}})
		raise Http404()
	return HttpResponse('OK')
