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
		#responder_usuario({u'message': {u'message_id': 1843,u'from': {u'id': 16850154, u'first_name': u'\u043c\u03b5\u043d\u044f\u03b1\u03b7\u03b5\u043d\u2728\U0001f343', u'username': u'Mehraneh_M'}, u'chat': {u'id': 16850154, u'first_name': u'\u043c\u03b5\u043d\u044f\u03b1\u03b7\u03b5\u043d\u2728\U0001f343', u'username': u'Mehraneh_M'}, u'text': u'/start', u'date': 1436759922}, u'update_id': 25202971})
		raise Http404()
	return HttpResponse('OK')
