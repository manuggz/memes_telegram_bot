from django.db import models


class Usuario(models.Model):
    id_u = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=200,default="NoName")
    apellido = models.CharField(max_length=200, null=True)
    nombreusuario = models.CharField(max_length=200, null=True)
    is_suscrito_actu = models.BooleanField(default=True)
    ultima_respuesta = models.ForeignKey("RespuestaServidor",null=True,on_delete=models.SET_NULL)
    datos_imagen_borrador  = models.ForeignKey("DatosImagenBorrador", null=True, on_delete=models.SET_NULL)
    comando_en_espera = models.CharField(max_length=200,default="None")

    def __str__(self):
        str_r = self.nombre

        if self.nombreusuario:
            str_r += "( " + self.nombreusuario + " )"
        return str_r


class DatosImagenBorrador(models.Model):
    upper_text = models.CharField(max_length=200, null=True,default="Upper TEXT")
    lower_text = models.CharField(max_length=200, null=True,default="Lower TEXT")
    color = models.CharField(max_length=200, null=True,default="white")

    def __str__(self):
        str_r = self.upper_text + " , " + self.lower_text + " , " + self.color
        return str_r


#Ultima Respuesta mandada por el servidor al usuario / Notar que
# respuestas de texto como a /start no cuentan porque hay restricciones a la capacidad de la BD
# solo se guardan las respuestas a /random /search <meme> o <meme> ya que es necesario
# para cuando el usuario utilize /next o /create , necesitamos guardar esas referencias
# Por eso SIEMPRE un usuario apunta A UN SOLO OBJETO RespuestaServidor
class RespuestaServidor(models.Model):
    usuario_t = models.ForeignKey(Usuario,primary_key=True)  # A Quien se envia el mensaje
    fecha = models.DateTimeField()  # Fecha de respuesta
    imagen_enviada = models.ForeignKey("Imagen",on_delete=models.CASCADE)  # Imagen enviada

    def __str__(self):
        str_r = str(self.usuario_t)
        return str_r


class Imagen(models.Model):
    title = models.CharField(max_length=200,default="")
    url_imagen = models.CharField(max_length=200)
    textobuscado = models.CharField(max_length=200)  # Texto buscado para acceder a la imagen
    # Ruta de la imagen en el servidor(in case) No es usada como debe ser al final
    ruta_imagen = models.CharField(max_length=200)
    id_lista = models.IntegerField()  # ID en la lista de imagenes


    def __str__(self):
        str_r = self.url_imagen + ":" + self.textobuscado +  "(" + str(self.id_lista) + ")"
        return str_r


# Eliminar las imagenes que no estan referenciadas por los usuarios
#DELETE FROM "BotTelegram_imagen" as ima_del   WHERE textobuscado not in ( select ima.textobuscado from "BotTelegram_imagen" as ima where ima.id in (select imagen_enviada_id from "BotTelegram_respuestaservidor"));
