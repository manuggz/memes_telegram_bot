from django.contrib import admin
from .models import Usuario,Imagen,GrupoChat,RespuestaServidor

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Imagen)
admin.site.register(GrupoChat)
admin.site.register(RespuestaServidor)

