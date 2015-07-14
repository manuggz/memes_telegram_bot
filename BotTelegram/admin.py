from django.contrib import admin
from .models import Usuario , Mensaje,Imagen,NodoImagen,ListaImagen
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Mensaje)
admin.site.register(Imagen)
admin.site.register(NodoImagen)
admin.site.register(ListaImagen)
