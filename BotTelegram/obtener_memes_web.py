# Crea el objeto que registra la respuesta del servidor
# Solo se guardan las respuesta en imagen
from HTMLParser import HTMLParser
from os.path import basename
from os.path import join
from random import choice

import requests

from BotTelegram.models import Imagen

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
    todos = Imagen.objects.all()
    if todos.exists():
        return choice(todos)
    return None


# construye todos los objetos Imagen de la BD dada una lista de URL hacia las imagenes
def construir_imagenes(imagenes, txt_bu):
    imagendb = None

    for i in range(len(imagenes) - 1, -1, -1):
        url_ima = "http:" + imagenes[i].url
        path_archivo = join('staticfiles', basename(url_ima))  # Ruta en el servidor
        #print imagenes[i]
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
def buscar_imagenes(memeConsultado):
    try:
        peticion = requests.get(PAGINA_MEMES, params={'q': memeConsultado})
    except:
        return None

    if peticion.status_code != 200:
        return None
    parser = parseadorHTML()
    parser.feed(peticion.text)
    return parser.imagenes



class parseadorHTML(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.imagenes = []
        self.imagen_actual = None

    def handle_starttag(self, tag, attrs):
        if tag == "h3":
            #print tag ,attrs
            self.imagen_actual = ImagenWeb()

        if tag == "img":
            #print tag,attrs
            self.imagen_actual.url = dict(attrs)['src']
            self.imagenes.append(self.imagen_actual)
            #print self.imagen_actual
            self.imagen_actual = None

    def handle_data(self, data):
        if self.imagen_actual:
            #print "ASDASDASD", data
            if data.strip():
                self.imagen_actual.title = data

