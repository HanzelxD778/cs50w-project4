from django.contrib import admin
from .models import Chat, Cuenta, Curso, Entrega, Entregable, Foro, Material, Mensaje, RespuestaForo, Seccion

# Register your models here.
admin.site.register(Cuenta)
admin.site.register(Curso)
admin.site.register(Material)
admin.site.register(Foro)
admin.site.register(RespuestaForo)
admin.site.register(Chat)
admin.site.register(Mensaje)
admin.site.register(Entregable)
admin.site.register(Entrega)
admin.site.register(Seccion)