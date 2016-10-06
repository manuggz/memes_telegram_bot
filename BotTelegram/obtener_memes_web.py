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




# De las imagenes referenciadas en la BD obtiene una aleatoria
def obtener_imagen_random():
    todos = Imagen.objects.all()
    if todos.exists():
        return choice(todos)
    return None



# construye todos los objetos Imagen de la BD dada una lista de URL hacia las imagenes
def construir_imagenes(rutas_imagenes, txt_bu):
    imagendb = None

    for i in range(len(rutas_imagenes) - 1, -1, -1):
        url_ima = "http:" + rutas_imagenes[i]['src']
        path_archivo = join('staticfiles', basename(url_ima))  # Ruta en el servidor

        imagendb = Imagen(id_lista=i,
                          url_imagen=url_ima,
                          ruta_imagen=path_archivo,
                          textobuscado=txt_bu)
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
    return parser.rutas_imagenes



class parseadorHTML(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.rutas_imagenes = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.rutas_imagenes.append(dict(attrs))

