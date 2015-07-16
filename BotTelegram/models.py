from django.db import models

class Usuario(models.Model):
	id_u = models.IntegerField(primary_key = True)
	nombreusuario  = models.CharField(max_length=200 , null = True)
	nombre   = models.CharField(max_length=200)
	apellido = models.CharField(max_length=200)
	suscrito_actu = models.BooleanField(default = True)


class Imagen(models.Model):
	url_imagen  = models.CharField(max_length=200 , primary_key =  True)
	ruta_imagen = models.CharField(max_length=200)
	alt_mensaje =  models.CharField(max_length=200)

class NodoImagen(models.Model):
	id_lista    = models.IntegerField()
	mdimagen    = models.ForeignKey("Imagen")
	siguiente   = models.ForeignKey("NodoImagen",null = True)

class ListaImagen(models.Model):
	txt_buscado =  models.CharField(max_length=200 , primary_key = True)
	primero     =  models.ForeignKey("NodoImagen")


class Mensaje(models.Model):
	fecha         = models.DateTimeField()
	id_mensaje       = models.IntegerField(primary_key = True)
	update_id        = models.IntegerField()
	texto_enviado    = models.CharField(max_length=2000 , null = True)
	usuario          = models.ForeignKey(Usuario) #Quien envia el mensaje
	enviado = models.ForeignKey("NodoImagen",null = True)
