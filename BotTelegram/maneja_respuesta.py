#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
import requests
import shutil
import json
from HTMLParser import HTMLParser
from os.path import join,exists,basename,splitext
from models import Usuario ,Mensaje,Imagen,ListaImagen,NodoImagen
from random import random
from PIL import Image,ImageDraw,ImageFont

CODE_BOT = "119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg";
URL_TG_API = "https://api.telegram.org/bot" + CODE_BOT + "/";
PAGINA_MEMES = 'http://imgflip.com/memesearch'

def dibujar_texto_sobre_imagen(texto,draw,image,fposiciony,color):
	if texto == "": return

	tam = image.size[1] // 9
	fuente = ImageFont.truetype("staticfiles/Impact.ttf", tam)

	tam_d = draw.textsize(texto,font = fuente)

	while  tam_d[0] + image.size[0]//2 - tam_d[0]//2 > image.size[0] :
		del fuente
		tam -= 2
		fuente = ImageFont.truetype("staticfiles/Impact.ttf", tam)
		tam_d = draw.textsize(texto,font = fuente)


	try:
		draw.text((image.size[0]//2 - tam_d[0]//2,fposiciony(tam_d,image.size)),texto, font=fuente,fill = color)
	except ValueError:
		draw.text((image.size[0]//2 - tam_d[0]//2,fposiciony(tam_d,image.size)),texto, font=fuente,fill = "red")


def enviarMensajeTexto(chat_id,mensaje):
	requests.get(URL_TG_API + 'sendMessage',params={'chat_id' : chat_id,'text':mensaje})

def enviarMensajeImagen(chat_id,ruta_foto):
	files = {'photo': open(ruta_foto, 'rb')}	
	try:
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

def guardarImagen(imagen):
	if not exists(imagen.ruta_imagen):
		resp = requests.get(imagen.url_imagen, stream=True)

		with open(imagen.ruta_imagen, 'wb') as archivo_img:
		    shutil.copyfileobj(resp.raw, archivo_img)

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


def buscarImagenes(memeConsultado):
	try:
		peticion = requests.get(PAGINA_MEMES,params={'q':memeConsultado})
	except :
		None

	if peticion.status_code != 200:
		return None
	parser   = parseadorHTML()
	parser.feed(peticion.text)
	return parser.rutas_imagenes

def enviarMensajeStart(primer_nombre,username,chat_id):
	mensaje = "Hey " + u"\U0001f604 " + primer_nombre + \
		 	  (" (@" +username +")! "  if username else "") + \
	          ". I can send you memes. Just tell me which one typing  <meme name> and if I can remember it " + \
			  " I'll send you a picture." + \
			  "\n\nExample: Type yao ming . If you do, i'll send you yao ming's meme.\n wanna know more? type /help"
	enviarMensajeTexto(chat_id,mensaje)

def enviarMensajeHelp(primer_nombre,chat_id):
	mensaje = "Hey " + primer_nombre + ", I can send you pictures of memes.\n" + \
				  "Just tell me which one. Type its name."

	mensaje += "\n\nExamples of /sendme:\n" 
	mensaje += "/sendme forever alone ,Texto 1 - Texto 2 , blue\n" 
	mensaje += "/sendme forever alone ,Texto 1 , white\n" 
	mensaje += "/sendme forever alone \n" 

	mensaje += "\n\nExamples of this bot, type each line:\n" 
	mensaje += "forever alone\n" 
	mensaje += "/another\n" 
	mensaje += "/create Im alone\n" 
	mensaje += "/create Im alone - But with my dog\n"
	mensaje += "/create Im alone - But with my dog , black\n"
	mensaje += "\nIf you have any suggestions for my creator let him now at @manuggz."
	mensaje += "\n\nPlease if you like this bot , rate it at :https://telegram.me/storebot?start=memesbot"
	enviarMensajeTexto(chat_id,mensaje)


def construir_imagenes(rutas_imagenes,txt_bu):
	anterior = None
	for i in range(len(rutas_imagenes)-1,-1,-1):
		url_ima      = "http:" + rutas_imagenes[i]['src']
		path_archivo = join('staticfiles',basename(url_ima))

		try:
			imagendb = Imagen.objects.get(url_imagen = url_ima)
		except ObjectDoesNotExist:
			imagendb = Imagen(url_imagen = url_ima,
							  ruta_imagen = path_archivo,
							  alt_mensaje = rutas_imagenes[i]['alt'])
			imagendb.save()

		nodo = NodoImagen(id_lista    = i,
			  			  mdimagen    = imagendb,
			              siguiente   =anterior)
		nodo.save()

		anterior = nodo

	ListaImagen(txt_buscado = txt_bu,
				primero     =  nodo).save()

	return nodo

def buscarPrimeraImagen(texto,chat_id,nombre):
	primera_imagen = None
	try:
		primera_imagen = ListaImagen.objects.get(txt_buscado = texto).primero
	except ObjectDoesNotExist:

		imagenes       = buscarImagenes(texto)
		if imagenes == []:
			enviarMensajeTexto(chat_id,"I'm sorry " + u'\U0001f605' + " @" + nombre + \
									   ".\n I can't remember this meme( " + texto + " )!. Type /help.")
		elif imagenes == None:
			enviarMensajeTexto(chat_id,"Sorry , there is a problem getting your meme. Try again.")

		else:
			primera_imagen = construir_imagenes(imagenes,texto)

	return primera_imagen

def escribirEnviarMeme(comandos,imagen,chat_id,usuario_m):

	guardarImagen(imagen)

	imagen_pil = Image.open(imagen.ruta_imagen)
	draw_pil   = ImageDraw.Draw(imagen_pil)

	mensajes = comandos[1].split("-")
	tup  = ""
	tdown = ""
	if len(mensajes) == 1:
		tdown = mensajes[0]
	else:
		tup   = mensajes[0]
		tdown = mensajes[1]

	try:
		color = comandos[2]
	except IndexError:
		color = "red"

	dibujar_texto_sobre_imagen(tup,draw_pil,imagen_pil,(lambda td , sz : sz[0]  // 12 ),color)
	dibujar_texto_sobre_imagen(tdown,draw_pil,imagen_pil,(lambda td , sz : sz[1]  -td[1] - td[1]//2 ),color)
	ruta_tu = splitext(imagen.ruta_imagen)
	ruta_guardar = ruta_tu[0] + str(usuario_m.pk)  + str(random()) + \
				ruta_tu[1]

	imagen_pil.save(ruta_guardar)
	enviarMensajeImagen(chat_id,ruta_guardar)


def responder_usuario(consulta):

	texto_mensaje = consulta['message'].get('text',"")
	chat_id       = consulta['message']['from']['id']
	primer_nombre = consulta['message']['from'].get('first_name',"")
	username      = consulta['message']['from'].get('username',"")
	apellido      = consulta['message']['from'].get('last_name',"")
	if texto_mensaje == "/This_group_is_hacked_by_FATA_Leave_it_or_you_will_face_the_consequences" :
		return

	try:
		usuario_m = Usuario.objects.get(nombreusuario = username , 
									nombre = primer_nombre ,
									apellido = apellido)
	except ObjectDoesNotExist:
		usuario_m = Usuario(nombreusuario = username , 
							nombre = primer_nombre ,
							apellido = apellido)
		usuario_m.save()

	try:
		mensaje_m = Mensaje.objects.get(id_mensaje = consulta['message']['message_id'])
	except ObjectDoesNotExist:
		mensaje_m = Mensaje(id_mensaje = consulta['message']['message_id'] , 
							update_id = consulta['update_id'],
							texto_enviado = texto_mensaje,
							usuario = usuario_m)


	if not texto_mensaje:
		enviarMensajeTexto(chat_id,"I dunno what you mean \ud83d\ude05 . Type /help ")
	elif texto_mensaje == "/start":
		enviarMensajeStart(primer_nombre,username,chat_id)
	elif texto_mensaje == "/help":
		enviarMensajeHelp(primer_nombre,chat_id)
	elif texto_mensaje == "/help":
		enviarMensajeHelp(primer_nombre,chat_id)
	elif "/create" in texto_mensaje:
		comandos = texto_mensaje[7:].strip()

		if not comandos:
			enviarMensajeTexto(chat_id,"Please use this command to write over the current meme , " + \
										"use it this way , example: \n\n/create " + \
										"Texto to write- Texto optional , red\n\nType /help " + \
										"for more examples.")
		else:
			comandos = [ i.strip() for i in comandos.split(',') if i ]

			ulti_m_con_ima = Mensaje.objects.filter(usuario = usuario_m ,
												 enviado__isnull = False).order_by('update_id')

			if ulti_m_con_ima:
				ulti_m_con_ima = ulti_m_con_ima[len(ulti_m_con_ima)-1]
				try:
					comandos = ("",comandos[0],comandos[1])
				except IndexError:
					comandos = ("",comandos[0])
				escribirEnviarMeme(comandos,ulti_m_con_ima.enviado.mdimagen,chat_id,usuario_m)
			else:
				enviarMensajeTexto(chat_id,"First tell me which meme typing its name!\n" + \
											"")



	elif "/sendme" in texto_mensaje:
		comandos = texto_mensaje[7:].strip()

		if not  comandos:
			enviarMensajeTexto(chat_id,"Please use this command to write memes , " + \
										"use it this way , example: \n\n/sendme yao ming , " + \
										"Texto to write- Texto optional , red\n\nType /help " + \
										"for more examples.")
		else:

			comandos = [ i.strip() for i in comandos.split(',') if i ]
			print comandos

			imagen = buscarPrimeraImagen(comandos[0].strip(),chat_id,primer_nombre)

			if imagen:

				imagen = imagen.mdimagen

				if len(comandos) > 1 :
					escribirEnviarMeme(comandos,imagen,chat_id,usuario_m)
				else:
					enviarImagen(imagen,chat_id)

	elif texto_mensaje == "/another":
		ulti_m_con_ima = Mensaje.objects.filter(usuario = usuario_m ,
											 enviado__isnull = False).order_by('update_id')

		if ulti_m_con_ima:
			ulti_m_con_ima = ulti_m_con_ima[len(ulti_m_con_ima)-1]
			if ulti_m_con_ima.enviado.siguiente:
				if enviarImagen(ulti_m_con_ima.enviado.siguiente.mdimagen,chat_id) != 0:
					enviarMensajeTexto(chat_id,"Sorry , there was a problem , try again. ")
				else:
					mensaje_m.enviado = ulti_m_con_ima.enviado.siguiente

			else:
				enviarMensajeTexto(chat_id,"Sorry , there's no more images for your meme. \n")

		else:
				enviarMensajeTexto(chat_id,"First tell me which meme!")


	elif "iranid" in texto_mensaje:
		enviarMensajeTexto(chat_id,"Iranid te amo! " + u'\U0001f618')
	else:
		imagen = buscarPrimeraImagen(texto_mensaje.strip(),chat_id,primer_nombre)

		if imagen:
			enviarImagen(imagen.mdimagen,chat_id)

			mensaje_m.enviado = imagen

	mensaje_m.save()
# Fin responder

