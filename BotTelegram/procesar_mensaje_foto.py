## Se encarga de manejar las fotos que el usuario envia
import json
import requests
from os.path import basename, exists
from os.path import join
from BotTelegram.enviar_mensajes_usuario import URL_TG_API, CODE_BOT, guardar_imagen, guardar_imagen_respuesta_servidor
from BotTelegram.models import Usuario, Imagen
from BotTelegram.procesar_comandos import create_tg


## Procesa cuando el usuario envia una foto
def procesar_mensaje_foto(mensaje, xml_strings, is_debug):

    usuario = Usuario.objects.create(
        id_u=mensaje.user_from.id,
        nombreusuario=mensaje.user_from.username[:200],
        nombre=mensaje.user_from.first_name[:200],
        apellido=mensaje.user_from.last_name[:200]
    )

    photo_size = mensaje.photo.maximo_tam()

    if photo_size:
        r = requests.get(URL_TG_API + 'getFile',
                         params={"file_id": photo_size.file_id})
        respuesta = json.loads(r.text)

        if respuesta["ok"]:

            file_path_tg = respuesta["result"]["file_path"]
            file_path_servidor = join('staticfiles', basename(file_path_tg))
            photo_size.file_id = respuesta["result"]["file_id"]
            photo_size.file_size = respuesta["result"]["file_size"]

            try:  # si ya el usuario subio una imagen anterior la borramos
                imagenes = Imagen.objects.filter(textobuscado=mensaje.user_from.id,id_lista=-1)
                imagenes.delete()
            except Imagen.ObjectDoesNotExist:
                pass

            ## Creamos una nueva imagen en la bd
            imagen = Imagen(
                id_lista=-1,  ## dice que es del usuario
                url_imagen="https://api.telegram.org/file/bot" + CODE_BOT + "/" + file_path_tg,
                ruta_imagen=file_path_servidor,
                textobuscado=usuario.pk,
                title=mensaje.caption
            )
            imagen.save()

            guardar_imagen(imagen)

            if exists(file_path_servidor):
                usuario.comando_en_espera = "None"

                guardar_imagen_respuesta_servidor(mensaje.datetime, usuario, imagen,guardar_usuario = False)

                create_tg(mensaje.user_from.id,usuario,"",is_debug,xml_strings)

    usuario.save()
