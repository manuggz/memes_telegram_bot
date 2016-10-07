from django.db import models


class Usuario(models.Model):
    id_u = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=200,default="NoName")
    apellido = models.CharField(max_length=200, null=True)
    nombreusuario = models.CharField(max_length=200, null=True)
    is_suscrito_actu = models.BooleanField(default=True) # cambiar a "is_suscrito_actu"
    ultima_respuesta = models.ForeignKey("RespuestaServidor",null=True,on_delete=models.SET_NULL)

    def __str__(self):
        str_r = self.nombre

        if self.nombreusuario:
            str_r += "( " + self.nombreusuario + " )"
        return str_r


class GrupoChat(models.Model):
    id_chat = models.IntegerField(primary_key=True)
    nombrechat = models.CharField(max_length=200, null=True)
    is_suscrito_actu = models.BooleanField(default=True)

    def __str__(self):
        str_r = self.nombrechat
        return str_r

#Ultima Respuesta mandada por el servidor al usuario / Notar que
# respuestas de texto como a /start no cuentan porque hay restricciones a la capacidad de la BD
# solo se guardan las respuestas a /random /sendme <meme> o <meme> ya que es necesario
# para cuando el usuario utilize /another o /create , necesitamos guardar esas referencias
# Por eso SIEMPRE un usuario apunta A UN SOLO OBJETO RespuestaServidor
class RespuestaServidor(models.Model):
    usuario_t = models.ForeignKey(Usuario,primary_key=True)  # A Quien se envia el mensaje
    fecha = models.DateTimeField()  # Fecha de respuesta
    imagen_enviada = models.ForeignKey("Imagen")  # Imagen enviada

    def __str__(self):
        str_r = str(self.usuario_t)
        return str_r


class Imagen(models.Model):
    title = models.CharField(max_length=200,default="")
    url_imagen = models.CharField(max_length=200)
    textobuscado = models.CharField(max_length=200)  # Texto buscado para acceder a la imagen
    ruta_imagen = models.CharField(max_length=200)  # Ruta de la imagen en el servidor(in case)
    id_lista = models.IntegerField()  # ID en la lista de imagenes


    def __str__(self):
        str_r = self.url_imagen + ":" + self.textobuscado +  "(" + str(self.id_lista) + ")"
        return str_r

