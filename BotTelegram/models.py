from django.db import models

class Usuario(models.Model):
	id_u = models.IntegerField(primary_key = True)
	nombreusuario  = models.CharField(max_length=200 , null = True)
	nombre   = models.CharField(max_length=200, null = True)
	apellido = models.CharField(max_length=200, null = True)
	suscrito_actu = models.BooleanField(default = True)

class GrupoChat(models.Model):
	id_chat = models.IntegerField(primary_key = True)
	nombrechat  = models.CharField(max_length=200 , null = True)
	suscrito_actu = models.BooleanField(default = True)


class RespuestaServidor(models.Model):
	id_mensaje       = models.IntegerField(primary_key = True)
	fecha            = models.DateTimeField()
	usuario          = models.ForeignKey(Usuario) #Quien envia el mensaje
	imagen_enviada   = models.ForeignKey("Imagen")

class Imagen(models.Model):
	url_imagen    = models.CharField(max_length=200)
	ruta_imagen   = models.CharField(max_length=200)  # Ruta de la imagen en el servidor(in case)
	textobuscado  = models.CharField(max_length=200)
	id_lista = models.IntegerField()
