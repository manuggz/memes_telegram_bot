from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
import json
from maneja_respuesta import responder_usuario



# Create your views here.
def index(request):
	return render(request,'index.html')

@csrf_exempt
def responder_mensaje(request):

	if request.method == 'POST':
		consulta = json.loads(request.body)
		print consulta
		responder_usuario(consulta)
	else:
		raise Http404()

	return HttpResponse('OK')