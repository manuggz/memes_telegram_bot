from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^usuario/(?P<id_usuario>\d+)$', views.mostrarUsuario, name='usuarios'),
    url(r'^119646075:AAFsQGgw8IaLwvRZX-IBO9mgV3k048NpuMg/$', views.responder_mensaje, name='responder_mensaje'),
]