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
		#consulta = {u'update_id': 25202817, u'message':{u'date': 1436632509, u'chat': {u'username': u'manuggz', u'first_name': u'Manuel', u'last_name': u'Gonzalez', u'id': 109518141}, u'from': {u'username': u'manuggz', u'first_name': u'Manuel', u'last_name': u'Gonzalez', u'id': 109518141}, u'message_id': 1049, u'text': u'yao ming'}}
		responder_usuario(consulta)
	else:
		#updid = 25202827
		#ms_id = 1059
		#consulta = {u'update_id': updid, u'message':{u'date': 1436632509, u'chat': {u'username': u'manuggz', u'first_name': u'Manuel', u'last_name': u'Gonzalez', u'id': 109518141}, u'from': {u'username': u'manuggz', u'first_name': u'Manuel', u'last_name': u'Gonzalez', u'id': 109518141}, u'message_id': ms_id, u'text': u'yao ming'}}
		#responder_usuario(consulta)
		#updid += 1
		#ms_id += 1
		#consulta = {u'update_id': updid, u'message':{u'date': 1436632509, u'chat': {u'username': u'manuggz', u'first_name': u'Manuel', u'last_name': u'Gonzalez', u'id': 109518141}, u'from': {u'username': u'manuggz', u'first_name': u'Manuel', u'last_name': u'Gonzalez', u'id': 109518141}, u'message_id': ms_id, u'text': u'/sendme yaoming, hola'}}
		#responder_usuario(consulta)
		# updid += 1
		# ms_id += 1
		# consulta = {u'update_id': updid, u'message':{u'date': 1436632509, u'chat': {u'username': u'manuggz', u'first_name': u'Manuel', u'last_name': u'Gonzalez', u'id': 109518141}, u'from': {u'username': u'manuggz', u'first_name': u'Manuel', u'last_name': u'Gonzalez', u'id': 109518141}, u'message_id': ms_id, u'text': u'/another'}}
		# responder_usuario(consulta)
		# updid += 1
		# ms_id += 1
		# consulta = {u'update_id': updid, u'message':{u'date': 1436632509, u'chat': {u'username': u'manuggz', u'first_name': u'Manuel', u'last_name': u'Gonzalez', u'id': 109518141}, u'from': {u'username': u'manuggz', u'first_name': u'Manuel', u'last_name': u'Gonzalez', u'id': 109518141}, u'message_id': ms_id, u'text': u'/another'}}
		# responder_usuario(consulta)

		raise Http404()

	return HttpResponse('OK')