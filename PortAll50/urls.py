from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("portall", views.portall, name="portall"),
    path("registrarCurso", views.registrarCurso, name="registrarCurso")
]