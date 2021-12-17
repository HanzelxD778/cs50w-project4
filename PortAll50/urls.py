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
    path("agregarForo", views.agregarForo, name="agregarForo"),
    path("foro/<int:id_foro>", views.foro, name="foro"),
    path("respuestaForo", views.respuestaForo, name="respuestaForo"),
    path("agregarSeccion", views.agregarSeccion, name="agregarSeccion"),
    path("agregarEnlace", views.agregarEnlace, name="agregarEnlace"),
    path("editarPerfil", views.editarPerfil, name="editarPerfil"),
    path("perfilEditado", views.perfilEditado, name="perfilEditado"),
    path("calificarEntrega", views.calificarEntrega, name="calificarEntrega"),
    path("agregarEstudiantesCurso", views.agregarEstudiantesCurso, name="agregarEstudiantesCurso"),
    path("eliminarEstudiantesCurso", views.eliminarEstudiantesCurso, name="eliminarEstudiantesCurso"),
    path("editarEntregable", views.editarEntregable, name="editarEntregable"),
    path("eliminarCurso", views.eliminarCurso, name="eliminarCurso"),
    path("mensaje/<int:id_persona>", views.mensaje, name="mensaje"),
    path("chatCurso/<int:id_curso>", views.chatCurso, name="chatCurso"),
    path("finalizarCurso", views.finalizarCurso, name="finalizarCurso"),
    path("calificarForo/<int:id_foro>/<int:id_estudiante>", views.calificarForo, name="calificarForo"),
    path("notasCurso/<int:id_curso>", views.notasCurso, name="notasCurso"),
    path("agregarMensaje<int:id_chat>", views.agregarMensaje, name="agregarMensaje"),
    path("editarRespuestaForo/<int:id_respuestaForo>/<int:id_foro>", views.editarRespuestaForo, name="editarRespuestaForo"),
    path("editarCalificacionEntrega/<int:id_entrega>", views.editarCalificacionEntrega, name="editarCalificacionEntrega")
]
