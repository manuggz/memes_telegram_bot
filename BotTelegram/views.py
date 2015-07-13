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
		#responder_usuario({u'update_id': 25204401, u'message': {u'message_id': 3374, u'date': 1436796688, u'from': {u'username': u'Dariush_sanei', u'id': 88961987, u'first_name': u'\u062f\u0627\u0631\u06cc\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640 \u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0648\u0634 \u0635\u0627\u0646\u0650\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640 \u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0639\u06cc'}, u'text': u'Fuck', u'chat': {u'username': u'Dariush_sanei', u'id': 88961987, u'first_name': u'\u062f\u0627\u0631\u06cc\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640 \u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0648\u0634 \u0635\u0627\u0646\u0650\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640 \u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0640\u0639\u06cc'}}})
		raise Http404()
	return HttpResponse('OK')
