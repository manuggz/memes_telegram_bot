from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^mensajes/$', views.mostrar_mensajes, name='mensajes_todos'), #Muestra todos los mensajes registrados

    url(r'^usuarios/$', views.mostrar_usuarios, name='usuarios_todos'), # Muestra todos los  usuarios registrados
    url(r'^usuario/(?P<id_usuario>\d+)$', views.mostrar_usuario, name='usuarios'), #Muestra los datos de un usuario

    url(r'^imagenes/$', views.mostrar_imagenes, name='imagenes_todas'), # Muestra todos los  usuarios registrados
    url(r'^imagenes/(?P<id_imagen>\d+)$', views.mostrar_imagen, name='imagen'), #Muestra los datos de una imagen

    url(r'^webhook/$', views.webhook, name='webhook'),  # Establece/Muestra el WebHook
    url(r'^pokemon/$', views.pokemon, name='pokemon'),  # Establece/Muestra el WebHook

    url(r'^me/$', views.mostrar_me, name='me'),  # Muestra informacion sobre el bot

    # Url que atiende los mensajes enviados por el Api de Telegram
    url(r'^119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/$', views.atender_mensaje_usuario_tg, name='responder_mensaje'),
]