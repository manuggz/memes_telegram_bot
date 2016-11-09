import logging,requests
from HTMLParser import HTMLParser
from os.path import basename,join
from random import choice

from BotTelegram.enviar_mensajes_usuario import parsear_enviar_xml
from BotTelegram.models import Imagen
from django.conf import settings

logger = logging.getLogger("BotTelegram.error_meme_web")

# URL de la pagina usada para buscar los memes
PAGINA_MEMES = 'http://imgflip.com/memesearch'

class ImagenWeb:

    def __init__(self):
        self.title = ""
        self.url = ""

    def __str__(self):
        return self.title + "-" + self.url

# De las imagenes referenciadas en la BD obtiene una aleatoria
def obtener_imagen_random():
    todos = Imagen.objects.filter(id_lista__gte=1)
    if todos.exists():
        return choice(todos)
    return None


# construye todos los objetos Imagen de la BD dada una lista de URL hacia las imagenes
def construir_imagenes(imagenes, txt_bu):
    imagendb = None

    for i in range(len(imagenes) - 1, -1, -1):
        url_ima = "http:" + imagenes[i].url
        path_archivo = join('staticfiles', basename(url_ima))  # Posible ruta en el servidor
        imagendb = Imagen(
            id_lista=i,
            url_imagen=url_ima,
            ruta_imagen=path_archivo[:200],
            textobuscado=txt_bu[:200],
            title = imagenes[i].title[:200]
        )
        imagendb.save()

    return imagendb


# Busca TODAS las imagenes en la pagina web PAGINA_MEMES
# va guardando TODAS las rutas url en una lista y las regresa
def buscar_imagenes_web(meme_consultado):

    respuesta = requests.get(PAGINA_MEMES, params={'q': meme_consultado})

    if respuesta.status_code != 200:
        logger.error("Request :" + PAGINA_MEMES + "\n" +
                      "con los parametros:" + str({'q': meme_consultado}) + "\n")

        if settings.DEBUG:
            ## Notar que es para forzar que falle un caso de prueba
            raise Exception("Error en request a la meme web ")
        return None

    parser = parseadorHTML()
    parser.feed(respuesta.text)
    return parser.imagenes


# Obtiene la primera imagen asociada a un texto buscado por el usuario
# si ya alguien lo ha buscado antes se regresa la referencia al primer objeto Imagen de la lista
# sino, se buscan todas-> se construyen en la BD y se regresa el primer objeto Imagen
def buscar_primera_imagen(chat_id, meme_name, xml_strings):
    primera_imagen = None
    try:
        primera_imagen = Imagen.objects.get(id_lista=0, textobuscado=meme_name)
    except Imagen.ObjectDoesNotExist:

        imagenes = buscar_imagenes_web(meme_name)

        if imagenes == []:
            parsear_enviar_xml(chat_id, xml_strings.find("no_recuerda_meme"))
        elif imagenes == None:
            parsear_enviar_xml(chat_id, xml_strings.find("problema_buscando_meme"))
        else:
            primera_imagen = construir_imagenes(imagenes, meme_name)

    return primera_imagen




class parseadorHTML(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.imagenes = []
        self.imagen_actual = None

    def handle_starttag(self, tag, attrs):
        if tag == "h3":
            self.imagen_actual = ImagenWeb()

        if tag == "img":
            self.imagen_actual.url = dict(attrs)['src']
            self.imagenes.append(self.imagen_actual)
            self.imagen_actual = None

    def handle_data(self, data):
        if self.imagen_actual:
            if data.strip():
                self.imagen_actual.title = data

