# coding=utf-8
from django.db import models


class Usuario(models.Model):
    id_u = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=200,default="NoName")
    apellido = models.CharField(max_length=200, null=True)
    nombreusuario = models.CharField(max_length=200, null=True)
    is_suscrito_actu = models.BooleanField(default=True)

    # Última imagen enviada como respuesta del servidor
    # O imagen enviada al bot
    imagen_actual = models.ForeignKey("Imagen",on_delete=models.SET_NULL,null=True)
    fecha_ultima_respuesta = models.DateTimeField(null=True)  # Fecha de respuesta/subida

    # Comando que espera respuesta del usuario
    comando_en_espera = models.CharField(max_length=200,default="None")

    # Datos del borrador usando /create

    esta_creando_meme = models.BooleanField(default=False)
    upper_text = models.CharField(max_length=200,default="Upper TEXT")
    lower_text = models.CharField(max_length=200, default="Lower TEXT")
    color = models.CharField(max_length=200, default="white")

    def __str__(self):
        str_r = self.nombre

        if self.nombreusuario:
            str_r += "( " + self.nombreusuario + " )"
        return str_r


class Imagen(models.Model):
    title = models.CharField(max_length=200,default="",blank=True,null=True)
    url_imagen = models.CharField(max_length=200)
    textobuscado = models.CharField(max_length=200)  # Texto buscado para acceder a la imagen
    # Ruta de la imagen en el servidor(in case) No es usada como debe ser al final
    ruta_imagen = models.CharField(max_length=200)
    id_lista = models.IntegerField(default=-1)  # ID en la lista de imagenes

    def __str__(self):
        str_r = self.url_imagen + ":" + self.textobuscado +  "(" + str(self.id_lista) + ")"
        return str_r



