from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from models import Usuario ,Mensaje,Imagen,ListaImagen,NodoImagen
import json
from maneja_respuesta import responder_usuario



# Create your views here.
def index(request):
	return render(request,'index.html',{'mensajes':Mensaje.objects.all()})

@csrf_exempt
def responder_mensaje(request):

	if request.method == 'POST':
		consulta = json.loads(request.body)
		print consulta
		responder_usuario(consulta)
	else:
		
		responder_usuario({u'message': {u'message_id': 3164,u'from': {u'id': 90747282, u'username': u'Ali_st80', u'last_name': u'St', u'first_name': u'Ali'}, u'date': 1436787442, u'text': u'/help', u'chat': {u'id': 90747282, u'username': u'Ali_st80', u'last_name': u'St', u'first_name': u'Ali'}}, u'update_id': 25204292})
		raise Http404()
	return HttpResponse('OK')
