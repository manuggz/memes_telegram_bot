from django.db import models


class Usuario(models.Model):
    id_u = models.IntegerField(primary_key=True)
    nombreusuario = models.CharField(max_length=200, null=True)
    nombre = models.CharField(max_length=200, null=True)
    apellido = models.CharField(max_length=200, null=True)
    suscrito_actu = models.BooleanField(default=True)

    def __str__(self):
        str_r = self.nombre

        if self.nombreusuario:
            str_r += "( " + self.nombreusuario + " )"
        return str_r


class GrupoChat(models.Model):
    id_chat = models.IntegerField(primary_key=True)
    nombrechat = models.CharField(max_length=200, null=True)
    suscrito_actu = models.BooleanField(default=True)

    def __str__(self):
        str_r = self.nombrechat
        return str_r


class RespuestaServidor(models.Model):
    id_mensaje = models.IntegerField(primary_key=True)
    fecha = models.DateTimeField()  # Fecha de respuesta
    usuario = models.ForeignKey(Usuario)  # Quien envia el mensaje
    imagen_enviada = models.ForeignKey("Imagen")  # Imagen enviada


    def __str__(self):
        str_r = self.id_mensaje
        return str_r


class Imagen(models.Model):
    url_imagen = models.CharField(max_length=200)
    ruta_imagen = models.CharField(max_length=200)  # Ruta de la imagen en el servidor(in case)
    textobuscado = models.CharField(max_length=200)  # Texto buscado para acceder a la imagen
    id_lista = models.IntegerField()  # ID en la lista de imagenes


    def __str__(self):
        str_r = self.url_imagen + ":" + self.textobuscado +  "(" + str(self.id_lista) + ")"
        return str_r

