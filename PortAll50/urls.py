from os import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("portall", views.portall, name="portall"),
    path("registrarCurso", views.registrarCurso, name="registrarCurso"),
    path("agregarCurso", views.agregarCurso, name="agregarCurso"),
    path("curso/<int:id_curso>", views.curso, name="curso"),
    path("agregarMaterial", views.agregarMaterial, name="agregarMaterial"),
    path("agregarEntregable", views.agregarEntregable, name="agregarEntregable"),
    path("entregable/<int:id_entregable>", views.entregable, name="entregable"),
    path("agregarEntrega", views.agregarEntrega, name="agregarEntrega"),
    path("agregarForo", views.agregarForo, name="agregarForo")
]
