from django.db import models
# help - Shows a text help
# another - Another image for your meme
# start - a starting message 

class Usuario(models.Model):
	nombreusuario  = models.CharField(max_length=50 , null = True)
	nombre   = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)


class Imagen(models.Model):
	url_imagen  = models.CharField(max_length=100 , primary_key =  True)
	ruta_imagen = models.CharField(max_length=50)
	alt_mensaje =  models.CharField(max_length=100)

class NodoImagen(models.Model):
	id_lista    = models.IntegerField()
	mdimagen    = models.ForeignKey("Imagen")
	siguiente   = models.ForeignKey("NodoImagen",null = True)

class ListaImagen(models.Model):
	txt_buscado =  models.CharField(max_length=100 , primary_key = True)
	primero     =  models.ForeignKey("NodoImagen")


class Mensaje(models.Model):
	#fecha         = models.CharField(max_length=200)
	id_mensaje       = models.IntegerField(primary_key = True)
	update_id        = models.IntegerField()
	texto_enviado    = models.CharField(max_length=300 , null = True)
	usuario          = models.ForeignKey(Usuario) #Quien envia el mensaje
	enviado = models.ForeignKey("NodoImagen",null = True)
