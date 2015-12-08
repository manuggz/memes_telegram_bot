from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^moteles/$', views.mostrarMoteles, name='moteles_todos'),
    url(r'^mensajes/$', views.mostrarMensajes, name='mensajes_todos'),
    url(r'^usuarios/$', views.mostrarUsuarios, name='usuarios_todos'),
    url(r'^usuario/(?P<id_usuario>\d+)$', views.mostrarUsuario, name='usuarios'),
    url(r'^119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/$', views.responder_mensaje, name='responder_mensaje'),
]