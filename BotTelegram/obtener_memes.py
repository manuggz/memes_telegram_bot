# coding=utf-8
import logging, requests
from HTMLParser import HTMLParser
from os.path import basename, join
from random import choice

from django.core.exceptions import ObjectDoesNotExist

from BotTelegram.enviar_mensajes_usuario import parsear_enviar_xml
from BotTelegram.models import Imagen
from django.conf import settings

logger = logging.getLogger("BotTelegram.error_meme_web")

# URL de la pagina usada para buscar los memes
URL_PAGINA_MEMES = 'http://imgflip.com/memesearch'


class ImagenWeb:
    """Abstrae una imagen de la pagina"""

    def __init__(self):
        self.title = ""
        self.url = ""

    def __str__(self):
        return self.title + "-" + self.url


class ParseadorHTML(HTMLParser):
    """Encargado de parsear la pagina web resultado del query.
    Crea una lista con las imagenes(ImagenWeb) encontradas"""

    def __init__(self):
        HTMLParser.__init__(self)
        self.imagenes = []  # Lista de Imagenes encontradas
        self.imagen_actual = None  # Imagen actual que se está parseando

    def handle_starttag(self, tag, attrs):
        if tag == "h3":  # Indicador que se encontró una imagen
            self.imagen_actual = ImagenWeb()

        if tag == "img":
            # Le colocamos las propiedades a la imagen
            # <img> siempre viene después de <h3>
            self.imagen_actual.url = dict(attrs)['src']
            self.imagenes.append(self.imagen_actual)
            self.imagen_actual = None

    def handle_data(self, data):
        if self.imagen_actual:  # Si se encontro una imagen
            if data.strip():
                self.imagen_actual.title = data  # Capturamos el titulo


# Busca TODAS las imagenes en la pagina web URL_PAGINA_MEMES resultado de buscar meme_consultado
# regresa una lista de Imagenes(ImagenWeb) con los memes encontrados
def buscar_memes_web(meme_consultado):
    respuesta = requests.get(URL_PAGINA_MEMES, params={'q': meme_consultado})

    if respuesta.status_code != 200:
        logger.error("Request :" + URL_PAGINA_MEMES + "\n" +
                     "con los parametros:" + str({'q': meme_consultado}) + "\n")

        if settings.DEBUG:
            ## Notar que es para forzar que falle un caso de prueba
            raise Exception("Error en request a la meme web ")
        return None

    parser = ParseadorHTML()
    parser.feed(respuesta.text)
    return parser.imagenes


# Crea una lista de Imagenes(Imagen) en la BD, correspondiente al texto buscado(meme_buscado)
# Recibe una lista de Imagenes(imagenes:[ImagenWeb])
# Regresa la primera imagen de la lista
def construir_imagenes(imagenes, meme_buscado):
    imagendb = None

    # i va desde (N - 1) hasta 0
    for i in range(len(imagenes) - 1, -1, -1):
        url_ima = "http:" + imagenes[i].url
        # Posible ruta cuando se quiera guardar en el servidor
        path_archivo = join('staticfiles', basename(url_ima))
        imagendb = Imagen(
            url_imagen=url_ima,
            ruta_imagen=path_archivo[:200],
            textobuscado=meme_buscado[:200],
            title=imagenes[i].title[:200],
            id_lista=i
        )
        imagendb.save()

    return imagendb


# De las imagenes referenciadas en la BD obtiene una aleatoria
def obtener_imagen_random():
    # id_lista__gte=0 (id_lista >= 0) porque las imagenes que sube el usuario se guardan con id_lista=-1
    todos = Imagen.objects.filter(id_lista__gte=0)
    return choice(todos) if todos.exists() else None


# Obtiene la primera imagen asociada a un texto buscado por el usuario
# si ya alguien lo ha buscado antes se regresa la referencia al primer objeto Imagen de la lista
# sino: se buscan todas-> se construyen en la BD y se regresa el primer objeto Imagen
def buscar_primera_imagen(chat_id, meme_name, xml_strings):

    try:  # Intentamos buscarla en la BD
        return Imagen.objects.get(id_lista=0, textobuscado=meme_name.strip())
    except ObjectDoesNotExist:  # No se ha buscado antes, se busca en la WEB
        pass

    imagenes = buscar_memes_web(meme_name)  # Se buscan los memes en la pagina web

    if imagenes == []:  # Si no se encontro ninguno
        parsear_enviar_xml(chat_id, xml_strings.find("no_recuerda_meme"))
    elif imagenes == None:  # Si ocurrio un error
        parsear_enviar_xml(chat_id, xml_strings.find("problema_buscando_meme"))
    else:  # si se consiguieron resultados
        return construir_imagenes(imagenes, meme_name)  # Se construyen en la BD
