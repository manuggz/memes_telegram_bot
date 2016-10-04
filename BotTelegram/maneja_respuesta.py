#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
import requests
import shutil
import json
from HTMLParser import HTMLParser
from os.path import join,exists,basename,splitext
from models import Usuario ,Imagen,RespuestaServidor
from random import random,randint,choice
import django.utils.timezone as timezone
from PIL import Image,ImageDraw,ImageFont
import datetime
from time import sleep

CODE_BOT = "119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg"
URL_TG_API = "https://api.telegram.org/bot" + CODE_BOT + "/"
PAGINA_MEMES = 'http://imgflip.com/memesearch'
FUENTE = "staticfiles/Montserrat-ExtraBold.otf"

def dibujar_texto_sobre_imagen(texto,draw,image,fposiciony,color):
	if texto == "": return

	tam = image.size[1] // 9
	fuente = ImageFont.truetype(FUENTE, tam)

	tam_d = draw.textsize(texto,font = fuente)

	while  tam_d[0] + image.size[0] // 2 - tam_d[0] // 2 > image.size[0] :
		del fuente
		tam -= 2
		fuente = ImageFont.truetype(FUENTE, tam)
		tam_d = draw.textsize(texto,font = fuente)


	try:
		draw.text((image.size[0] // 2 - tam_d[0] // 2,fposiciony(tam_d,image.size)),texto, font=fuente,fill = color)
	except ValueError:
		draw.text((image.size[0] // 2 - tam_d[0] // 2,fposiciony(tam_d,image.size)),texto, font=fuente,fill = "red")


def enviarMensajeTexto(chat_id,mensaje):
	requests.get(URL_TG_API + 'sendChatAction',params={'chat_id' : chat_id,'action':'typing'})
	sleep(2)
	requests.get(URL_TG_API + 'sendMessage',params={'chat_id' : chat_id,'text':mensaje})

def enviarMensajeImagen(chat_id,ruta_foto):
	files = {'photo': open(ruta_foto, 'rb')}	
	try:
		requests.get(URL_TG_API + 'sendChatAction',params={'chat_id' : chat_id,'action':'upload_photo'})
		r = requests.post(URL_TG_API + "sendPhoto",data={'chat_id':chat_id},files=files)
	except:
		return -1

	if r.status_code != 200:
		print r.text
		return -1

	respuesta = json.loads(r.text)
	if not respuesta["ok"]:
		print r.text
		return 1

	return 0

#Si no existe la imagen en el servidor
# la guarda en la ruta especificada
def guardarImagen(imagen):
	if not exists(imagen.ruta_imagen):
		resp = requests.get(imagen.url_imagen, stream=True)

		with open(imagen.ruta_imagen, 'wb') as archivo_img:
		    shutil.copyfileobj(resp.raw, archivo_img)

#envia una imagen a un chat
#notar que primero se debe guardar la imagen localmente
def enviarImagen(imagen,chat_id):
	guardarImagen(imagen)
	return enviarMensajeImagen(chat_id,imagen.ruta_imagen)


class parseadorHTML(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.rutas_imagenes = []

	def handle_starttag(self, tag, attrs):
		if tag == "img":
			self.rutas_imagenes.append(dict(attrs))

#Busca TODAS las imagenes en la pagina web PAGINA_MEMES
# va guardando TODAS las rutas url en una lista y las regresa
def buscarImagenes(memeConsultado):
	try:
		peticion = requests.get(PAGINA_MEMES,params={'q':memeConsultado})
	except :
		return None

	if peticion.status_code != 200:
		return None
	parser = parseadorHTML()
	parser.feed(peticion.text)
	return parser.rutas_imagenes

def  enviarMensajeATodosUsuarios(mensaje):
	usuarios = Usuario.objects.all()

	for usuario in usuarios:
		if usuario.suscrito_actu:
			enviarMensajeTexto(usuario.pk , mensaje)

def obtenerImagenRandom():
	todos = list(Imagen.objects.all())
	return  choice(Imagen.objects.all())

def enviarMensajeStart(primer_nombre,username,chat_id):
	mensaje = "Hey " + u"\U0001f604 " + primer_nombre + \
		 	  (" (@" + username + ")! "  if username else "") + \
	          ". I can send you memes. Just tell me which one typing  <meme name> and if I can remember it " + \
			  " I'll send you a picture." + \
			  "\n\nExample: Send me yao ming . If you do, i'll send you yao ming's meme.\n wanna know more? Send me /help"
	enviarMensajeTexto(chat_id,mensaje)

def enviarMensajeHelpCommands(primer_nombre,username,chat_id):
	mensaje = "Hey " + u"\U0001f604 " + primer_nombre + \
		 	  (" (@" + username + ")! "  if username else "") + \
	          " to do your meme i just need two things : Text to write and a color. \n" + \
	          "Give me those things like this : Text to write - Optional Text to write , COLOR\n" + \
	          "I use the comma(,) to separate the text and the color and the hyphen(-) to separate" + \
	          " the upper and lower text." 
	enviarMensajeTexto(chat_id,mensaje)

def enviarMensajeHelp(comando,chat_id):

	if comando == "sendme":
		mensaje = """
To use this command you have to tell me three things, which meme you want me to fetch, a text to write over your meme and a color to use.

The format is: /sendme MEME , TEXT 1 - TEXT 2 , COLOR

Text 1 : upper text
Text 2 : optional lower text , if you dont tell me a Text 2 , then Text 1 will be written on the lower part.

Color: it is a string , tell me a color name if I dont know it, i'll write using RED.

Notice that Text 1 and Text 2 are separated using a hyphen(-) , and the texts and color are separated using a comma(,) that have to be respected.""" 
		enviarMensajeTexto(chat_id,mensaje)
	elif comando == "create":
		mensaje = """
To use this command you have to tell me two things ,  a text to write over your meme and a color to use.

The format is: /create TEXT 1 - TEXT 2 , COLOR

Text 1 : upper text
Text 2 : optional lower text , if you dont tell me a Text 2 , then Text 1 will be written on the lower part.

This command use your current meme that you got using /sendme MEME or just typing its name.

Color: it is a string , tell me a color name if I dont know it, i'll write using RED.

Notice that Text 1 and Text 2 are separated using a hyphen(-) , and the texts and color are separated using a comma(,) that have to be respected."""			
		enviarMensajeTexto(chat_id,mensaje)
	elif comando == "random":
		mensaje = """
		Get a random meme"""
		enviarMensajeTexto(chat_id,mensaje)
	else:

		mensaje = "Hey" + ", I can send you pictures of memes.\n" + \
					  "Just tell me which one. Send me its name."

		mensaje += "\n\nExamples of /sendme:\n" 
		mensaje += "/sendme forever alone ,Texto 1 - Texto 2 , blue\n" 
		mensaje += "/sendme forever alone ,Texto 1 , white\n" 
		mensaje += "/sendme forever alone \n" 
		mensaje += "For more information : Send me /help sendme\n" 

		mensaje += "\n\nExamples of this bot, Send me each line:\n" 
		mensaje += "forever alone\n" 
		mensaje += "/another\n" 
		mensaje += "/create Im alone\n" 
		mensaje += "/create Im alone - But with my dog\n"
		mensaje += "/create Im alone - But with my dog , black\n"
		mensaje += "For more information : Send me /help create\n\n" 
		mensaje += "\nIf you have any suggestions for my creator let him now at @manuggz."
		mensaje += "\n\nPlease if you like this bot , rate it at :https://telegram.me/storebot?start=memesbot"
		enviarMensajeTexto(chat_id,mensaje)


#construye todos los objetos Imagen de la BD dada una lista de URL hacia las imagenes
def construir_imagenes(rutas_imagenes,txt_bu):

	for i in range(len(rutas_imagenes) - 1,-1,-1):
		url_ima = "http:" + rutas_imagenes[i]['src']
		path_archivo = join('staticfiles',basename(url_ima)) #Ruta en el servidor

		imagendb = Imagen(id_lista = i,
						  url_imagen = url_ima,
						  ruta_imagen = path_archivo,
						  textobuscado = txt_bu)		
		imagendb.save()

	return imagendb

#Obtiene la primera imagen asociada a un texto buscado por el usuario
#si ya alguien lo ha buscado antes se regresa la referencia al primer objeto Imagen de la lista
#sino, se buscan todas-> se construyen en la BD y se regresa el primer objeto Imagen
def buscarPrimeraImagen(texto,chat_id,nombre):
	primera_imagen = None
	try:
		primera_imagen = Imagen.objects.get(id_lista = 0 , textobuscado = texto)
	except ObjectDoesNotExist:

		imagenes = buscarImagenes(texto)
		if imagenes == []:
			enviarMensajeTexto(chat_id,"I'm sorry " + u'\U0001f605' + " @" + nombre + \
									   ".\n I can't remember this meme( " + texto + " )!. Send me /help.")
		elif imagenes == None:
			enviarMensajeTexto(chat_id,"Sorry , there is a problem getting your meme. Try again.")

		else:
			primera_imagen = construir_imagenes(imagenes,texto)

	return primera_imagen

def escribirEnviarMeme(comandos,imagen,chat_id,usuario_m):

	guardarImagen(imagen)

	imagen_pil = Image.open(imagen.ruta_imagen)
	draw_pil = ImageDraw.Draw(imagen_pil)

	mensajes = comandos[1].split("-")
	tup = ""
	tdown = ""
	if len(mensajes) == 1:
		tdown = mensajes[0]
	else:
		tup = mensajes[0]
		tdown = mensajes[1]

	try:
		color = comandos[2]
	except IndexError:
		color = "red"

	dibujar_texto_sobre_imagen(tup,draw_pil,imagen_pil,(lambda td , sz : sz[0] // 12),color)
	dibujar_texto_sobre_imagen(tdown,draw_pil,imagen_pil,(lambda td , sz : sz[1] - td[1] - td[1] // 2),color)
	ruta_tu = splitext(imagen.ruta_imagen)
	ruta_guardar = ruta_tu[0] + str(usuario_m.pk) + str(random()) + \
				".PNG"

	imagen_pil.save(ruta_guardar, quality=95)
	enviarMensajeImagen(chat_id,ruta_guardar)


def responder_usuario(consulta):

	texto_mensaje = consulta['message'].get('text',"")
	chat_id = consulta['message']['chat']['id']
	user_id = consulta['message']['from']['id']
	primer_nombre = consulta['message']['from'].get('first_name',"")
	username = consulta['message']['from'].get('username',"")
	apellido = consulta['message']['from'].get('last_name',"")
	fecha_m = consulta['message']['date']
	es_grupo = consulta['message']['chat']['id'] != consulta['message']['from']['id']

	if es_grupo:
		titulo_chat = consulta['message']['chat']['title']

	if texto_mensaje == "/This_group_is_hacked_by_FATA_Leave_it_or_you_will_face_the_consequences" :
		return

	try:
		usuario_m = Usuario.objects.get(id_u = user_id)
	except ObjectDoesNotExist: #Agregamos el nuevo usuario :D
		usuario_m = Usuario(id_u       = user_id,
							nombreusuario = username[:200], 
							nombre   = primer_nombre[:200] ,
							apellido = apellido[:200])
		usuario_m.save()

	try:
		RespuestaServidor.objects.get(id_mensaje = consulta['message']['message_id'])
		return #Mensaje ya respondido
	except ObjectDoesNotExist:
		pass


	if not texto_mensaje:

		#This is not working!
		if consulta.get('new_chat_participant',None):
			if consulta['new_chat_participant']['username'] == 'MemesBot':
				enviarMensajeHelp("",chat_id)
			else:
				enviarMensajeTexto(chat_id,"Hi " + username + " , new friend!. Send me /help ")

	elif texto_mensaje[0:6] == "/start":
		if not es_grupo or texto_mensaje[7:] == 'MemesBot':
			enviarMensajeStart(primer_nombre,username,chat_id)
	elif texto_mensaje[0:5] == "/help":
		if es_grupo and texto_mensaje[6:] == 'MemesBot':
			enviarMensajeHelp(texto_mensaje[14:].strip(),chat_id)
		elif not es_grupo:
			enviarMensajeHelp(texto_mensaje[5:].strip(),chat_id)
	elif texto_mensaje[0:7] == "/random":
		if not es_grupo or texto_mensaje[8:] == 'MemesBot':
			im_ale = obtenerImagenRandom()
			enviarImagen(im_ale,chat_id)
			respuesta = RespuestaServidor(id_mensaje = consulta['message']['message_id'],
								fecha=timezone.make_aware(datetime.datetime.utcfromtimestamp(int(fecha_m)),
								timezone.get_default_timezone()),
								usuario = usuario_m,
								imagen_enviada = im_ale)
			respuesta.save()

	elif texto_mensaje[0:5] == "/stop":
		if not es_grupo or texto_mensaje[6:] == 'MemesBot':
			if not  usuario_m.suscrito_actu:
				enviarMensajeTexto(chat_id,"You just dont like me right? You were already out of the queue.")
			else:
				usuario_m.suscrito_actu = False
				usuario_m.save()
				enviarMensajeTexto(chat_id,"Now, you won't receive my updates and any other messages.")
	elif texto_mensaje[0:17] == "/wannaknowupdates":
		if not es_grupo or texto_mensaje[18:] == 'MemesBot':
			if not  usuario_m.suscrito_actu:
				usuario_m.suscrito_actu = True
				usuario_m.save()
				enviarMensajeTexto(chat_id,"Hello again ,now you will receive update notifications.")
			else:
				enviarMensajeTexto(chat_id,"You are already receiving my notifications.")

	elif texto_mensaje[0:7] == "/create":
		comandos = ""
		valido = False
		if not es_grupo:
			comandos = texto_mensaje[8:].strip()
			valido = True
		else:
			if texto_mensaje[8:16] == 'MemesBot':
				comandos = texto_mensaje[17:].strip()
				valido = True

		if valido:
			if not comandos :
				enviarMensajeTexto(chat_id,"Please use this command to write over the current meme , " + \
											"use it this way , example: \n\n/create " + \
											"Texto to write- Texto optional , red\n\nSend me /help " + \
											"for more examples.")
			else:
				comandos = [ i.strip() for i in comandos.split(',') if i ]

				ulti_m_con_ima = RespuestaServidor.objects.filter(usuario = usuario_m).order_by('id_mensaje')

				if ulti_m_con_ima:
					ulti_m_con_ima = ulti_m_con_ima[len(ulti_m_con_ima) - 1]
					try:
						comandos = ("",comandos[0],comandos[1])
					except IndexError:
						comandos = ("",comandos[0])
					escribirEnviarMeme(comandos,ulti_m_con_ima.imagen_enviada,chat_id,usuario_m)
				else:
					enviarMensajeTexto(chat_id,"First tell me which meme typing its name!\n" + \
												"")

	elif texto_mensaje[0:7] == "/sendme":
		comandos = ""
		valido = False
		if not es_grupo:
			comandos = texto_mensaje[8:].strip()
			valido = True
		else:
			if texto_mensaje[8:16] == 'MemesBot':
				comandos = texto_mensaje[17:].strip()
				valido = True

		if valido:
			if not  comandos:
				enviarMensajeTexto(chat_id,"Please use this command to write memes , " + \
											"use it this way , example: \n\n/sendme yao ming , " + \
											"Texto to write- Texto optional , red\n\nSend me /help " + \
											"for more examples.")
			else:

				comandos = [ i.strip() for i in comandos.split(',') if i ]
				#print comandos
				imagen = buscarPrimeraImagen(comandos[0].strip(),chat_id,primer_nombre)

				if imagen: #Si se encontro una imagen con exito
					if len(comandos) > 1 : #si el usuario quiere un texto sobre la imagen
						escribirEnviarMeme(comandos,imagen,chat_id,usuario_m)
					else: #si solo quiere la imagen cruda

						enviarImagen(imagen,chat_id) #Le enviamos la imagen
						
						#Notar que guardamos en el servidor la respuesta, esto es usable por /create y /another
						respuesta = RespuestaServidor(id_mensaje = consulta['message']['message_id'],
											fecha=timezone.make_aware(datetime.datetime.utcfromtimestamp(int(fecha_m)),
											timezone.get_default_timezone()),
											usuario = usuario_m,
											imagen_enviada = imagen)
						respuesta.save()

	elif texto_mensaje[0:8] == "/another":
		ulti_m_con_ima = RespuestaServidor.objects.filter(usuario = usuario_m).order_by('id_mensaje')

		if ulti_m_con_ima:
			ulti_m_con_ima = ulti_m_con_ima[len(ulti_m_con_ima) - 1]

			try:
				imagen_siguiente = Imagen.objects.get(id_lista =ulti_m_con_ima.imagen_enviada.id_lista + 1 , 
													  textobuscado = ulti_m_con_ima.imagen_enviada.textobuscado)

				requests.get(URL_TG_API + 'sendChatAction',params={'chat_id' : chat_id,'action':'upload_photo'})
				if enviarImagen(imagen_siguiente,chat_id) != 0:
					enviarMensajeTexto(chat_id,"Sorry , there was a problem , try again. ")
				else:
					#Guardamos en el servidor la respuesta, esto es usable por /create y /another
					respuesta = RespuestaServidor(id_mensaje = consulta['message']['message_id'],
										fecha=timezone.make_aware(datetime.datetime.utcfromtimestamp(int(fecha_m)),
										timezone.get_default_timezone()),
										usuario = usuario_m,
										imagen_enviada = imagen_siguiente)
					respuesta.save()

			except ObjectDoesNotExist:
				enviarMensajeTexto(chat_id,"Sorry , there's no more images for your meme. \n")

		else:
				enviarMensajeTexto(chat_id,"First tell me which meme!")
	else:
		if not es_grupo:
			imagen = buscarPrimeraImagen(texto_mensaje.strip(),chat_id,primer_nombre)

			if imagen:
				enviarImagen(imagen,chat_id)
				#Guardamos en el servidor la respuesta, esto es usable por /create y /another
				respuesta = RespuestaServidor(id_mensaje = consulta['message']['message_id'],
									fecha=timezone.make_aware(datetime.datetime.utcfromtimestamp(int(fecha_m)),
									timezone.get_default_timezone()),
									usuario = usuario_m,
									imagen_enviada = imagen)
				respuesta.save()

# Fin responder

