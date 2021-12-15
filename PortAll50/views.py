from typing import ChainMap
from django.http import HttpResponse, request
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages #import messages
from django.contrib.auth.decorators import login_required
from . models import Cuenta, Curso, Entrega, Foro, Material, Entregable, RespuestaForo, Seccion, Url, Chat, Mensaje
from datetime import datetime
from decimal import Decimal

# Create your views here.
def index(request):
    return render(request, 'portall50/index.html')

def register(request):
    if request.method == "GET":
        return render(request, "portall50/register.html")
    else:
        first_name = request.POST["firstName"]
        last_name = request.POST["lastName"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        tipo_cuenta = request.POST.get("tipo_cuenta")
        imagen = request.FILES.get("txtImagen")

    if User.objects.filter(username=username).exists():
        return render(request, "portall50/register.html", messages.error(request, "User already exists D:" ))

    #https://docs.djangoproject.com/en/3.2/topics/auth/default/
    user = User.objects.create_user(username, email, password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    cuenta_user = Cuenta.objects.create(username=user, tipo=tipo_cuenta, imagen=imagen)

    messages.success(request, "User saved." )

    return HttpResponseRedirect(reverse("login"))

def portall(request):
    
    usuario = request.user

    cursos = Curso.objects.filter(cuentas=usuario)

    context = {
        "cursos": cursos,
        "usuario": Cuenta.objects.get(username=usuario)
    }

    return render(request, "portall50/portall.html", context)

def editarPerfil(request):
    usuario = request.user

    context = {
        "perfil": usuario
    }

    return render(request, "portall50/editarPerfil.html", context)

def perfilEditado(request):

    usuario_actual = request.user

    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    username = request.POST.get("username")
    password = request.POST.get("password")
    imagen = request.FILES.get("imagen")

    objeto_usuario = User.objects.get(username=usuario_actual)
    objeto_usuario_cuenta = Cuenta.objects.get(username=objeto_usuario)

    if first_name:
        objeto_usuario.first_name = first_name
    
    if last_name:
        objeto_usuario.last_name = last_name

    if email:
         objeto_usuario.email = email

    if username:
        objeto_usuario.username = username

    if password:
        objeto_usuario.set_password(password)

    if imagen:
        objeto_usuario_cuenta.imagen = imagen

    objeto_usuario_cuenta.save()
    objeto_usuario.save()

    print(objeto_usuario_cuenta)
    print(imagen)

    if password:
        return redirect("/accounts/logout")

    return redirect("/portall")

def agregarCurso(request):

    context = {
        "estudiantes": User.objects.filter(info_cuenta__tipo="1")
    }

    return render(request, "portall50/agregarCurso.html", context)

def registrarCurso(request):
    nombre_curso = request.POST.get("nombre_curso")
    estudiantes_curso = request.POST.getlist("estudiantes_curso")
    propietario_curso = request.POST.get("propietario_curso")
    txtImagen = request.FILES.get("txtImagen")

    total_acumular = request.POST.get("total_acumular")
    cantidad_minima = request.POST.get("cantidad_minima")

    propietario = User.objects.filter(pk=propietario_curso)

    propietario = propietario[0]

    #el objeto creado primero
    curso = Curso.objects.create(nombre_curso=nombre_curso, propietario=propietario, imagen=txtImagen, cantidad_minima=cantidad_minima, total_acumular=total_acumular)

    for estudianteID in estudiantes_curso:
        estudiante = User.objects.get(pk=estudianteID)

        if estudiante:
            curso.cuentas.add(estudiante)

    curso.cuentas.add(propietario)

    nombre_chat = f"Chat de {nombre_curso}"

    chatCurso = Chat.objects.create(nombre_chat=nombre_chat, curso=curso)

    return redirect("/portall")

def curso(request, id_curso):

    curso = Curso.objects.get(id=id_curso)

    context = {
        "curso": curso
    }

    return render(request, "PortAll50/curso.html", context)

def eliminarCurso(request):
    curso_id = request.POST.get("curso_id")

    curso = Curso.objects.get(id=curso_id)

    curso.delete()

    return redirect("/portall")

def agregarMaterial(request):
    nombre_material = request.POST.get("nombre_material")
    archivo = request.FILES.get("archivo")
    seccion_id = request.POST.get("seccion_id")
    id_curso = request.POST.get("curso_id")

    seccion = Seccion.objects.get(pk=seccion_id)

    material = Material.objects.create(nombre_material=nombre_material, archivo=archivo, seccion=seccion)

    print(id_curso)

    #return redirect("/portall")
    return redirect(f"curso/{id_curso}")

def agregarEntregable(request):
    nombre_entregable = request.POST.get("nombre_entregable")
    archivo = request.FILES.get("archivo")
    comentario = request.POST.get("comentario")
    date = request.POST.get("date")
    time = request.POST.get("time")
    seccion_id = request.POST.get("seccion_id")
    id_curso = request.POST.get("curso_id")

    nota = request.POST.get("nota")
    curso = Curso.objects.get(id=id_curso)

    total_acumular = curso.total_acumular
    actual_acumulado = curso.actual_acumulado

    actual_acumulado += Decimal(nota)

    if actual_acumulado > total_acumular:
        return redirect("/portall", messages.error(request, "No se puede agregar ese entregable porque supera la nota maxima del curso"))

    curso.actual_acumulado = actual_acumulado

    curso.save()

    seccion = Seccion.objects.get(pk=seccion_id)

    fecha_hora = f"{date}T{time}" 

    fecha = datetime.fromisoformat(fecha_hora)
    #datetime.fromisoformat('2011-11-04T00:05:23')

    entregable = Entregable.objects.create(nombre_entregable=nombre_entregable, archivo=archivo, comentario=comentario, tiempo_disp_hasta=fecha,seccion=seccion, nota=nota)

    return redirect(f"curso/{id_curso}")

def entregable(request, id_entregable):
    entregable = Entregable.objects.get(id=id_entregable)
    entregas = Entrega.objects.filter(entregable=entregable)
    estudiante = User.objects.get(username=request.user)

    try:
        entregas_usuario = Entrega.objects.filter(entregable=entregable)
    except:
        entregas_usuario = "8"

    for entrega in entregas_usuario:
        if entrega.cuenta == estudiante:
            envio = entrega

    #print(entregas_usuario)
    try:
        print(envio)
    except:
        envio = entregas_usuario

    context = {
        "entregable": entregable,
        "entregas": entregas,
        "entregas_usuario": entregas_usuario,
        "estudiante": estudiante,
        "envio": envio
    }

    return render(request, "PortAll50/entregable.html", context)

#Editar la tarea que sube el estudiante, se debería llamar editarEntrega
def editarEntregable(request):
    id_entregable = request.POST.get("id_entregable")
    archivo_entrega = request.FILES.get("archivo_entrega")

    entrega = Entrega.objects.get(id=id_entregable)

    entrega.archivo_entrega = archivo_entrega

    now = datetime.now()
    entrega.tiempo_entregado = now

    entrega.save()

    return redirect("/portall")

def agregarEntrega(request):
    archivo_entrega = request.FILES.get("archivo_entrega")
    id_entregable = request.POST.get("id_entregable")
    id_cuenta = request.POST.get("id_cuenta")
    estado_entrega = "0"

    entregable = Entregable.objects.get(id=id_entregable)

    cuenta = User.objects.get(id=id_cuenta)

    agregarEntrega = Entrega.objects.create(archivo_entrega=archivo_entrega, entregable=entregable, cuenta=cuenta, estado_entrega=estado_entrega)

    return redirect("/portall")

def agregarForo(request):
    nombre_foro = request.POST.get("nombre_foro")
    asignacion_foro = request.POST.get("asignacion_foro")
    date = request.POST.get("date")
    time = request.POST.get("time")
    seccion_id = request.POST.get("seccion_id")
    id_curso = request.POST.get("curso_id")

    nota = request.POST.get("nota")
    curso = Curso.objects.get(id=id_curso)

    total_acumular = curso.total_acumular
    actual_acumulado = curso.actual_acumulado

    actual_acumulado += Decimal(nota)

    if actual_acumulado > total_acumular:
        return redirect("/portall", messages.error(request, "No se puede agregar ese foro porque supera la nota maxima del curso"))

    curso.actual_acumulado = actual_acumulado

    curso.save()

    seccion = Seccion.objects.get(pk=seccion_id)
    
    fecha_hora = f"{date}T{time}" 

    fecha = datetime.fromisoformat(fecha_hora)
    #datetime.fromisoformat('2011-11-04T00:05:23')

    foro = Foro.objects.create(nombre_foro=nombre_foro, asignacion_foro=asignacion_foro, fecha_vencimiento=fecha, seccion=seccion, nota=nota)

    return redirect(f"curso/{id_curso}")

def foro(request, id_foro):
    user = request.user
    foro = Foro.objects.get(id=id_foro)
    respuestasForo = RespuestaForo.objects.filter(foro=foro)
    seccion = foro.seccion
    curso = seccion.curso

    context = {
        "user": user,
        "foro": foro,
        "respuestasForo": respuestasForo,
        "curso": curso
    }

    return render(request, "PortAll50/foro.html", context)

def respuestaForo(request):
    respuesa_foro = request.POST.get("respuesa_foro")
    id_foro = request.POST.get("id_foro")
    id_cuenta = request.POST.get("id_cuenta")

    foro = Foro.objects.get(id=id_foro)
    cuenta = User.objects.get(id=id_cuenta)

    entrega = RespuestaForo.objects.create(respuesa_foro=respuesa_foro, foro=foro, cuenta=cuenta.info_cuenta)

    return redirect("/portall")

def agregarSeccion(request):
    nombre_seccion = request.POST.get("nombre_seccion")
    curso_id = request.POST.get("curso_id")

    curso = Curso.objects.get(id=curso_id)

    seccion = Seccion.objects.create(nombre=nombre_seccion, curso=curso)

    return redirect("/portall")

def agregarEnlace(request):
    nombre_enlace = request.POST.get("nombre_enlace")
    url = request.POST.get("url")
    seccion_id = request.POST.get("seccion_id")
    id_curso = request.POST.get("curso_id")

    seccion = Seccion.objects.get(pk=seccion_id)

    url = Url.objects.create(nombre_enlace=nombre_enlace, url=url, seccion=seccion)

    print(id_curso)

    return redirect(f"curso/{id_curso}")

def calificarEntrega(request):
    id_entrega = request.POST.get("id_entrega")
    nota = request.POST.get("nota")

    entrega = Entrega.objects.get(id=id_entrega)
    
    if Decimal(nota) > entrega.entregable.nota:
        return redirect("/portall", messages.error(request, "No se puede poner esa calificación porque super la nota del entregable"))

    entrega.nota = nota
    
    entrega.estado_entrega = "1"

    entrega.save()

    return redirect("/portall")

def agregarEstudiantesCurso(request):
    username = request.POST.get("username")
    curso_id = request.POST.get("curso_id")

    curso = Curso.objects.get(id=curso_id)

    existe = False

    for estudiante in curso.cuentas.all():
        if estudiante.username == username:
            existe = True

    if existe:
        return redirect("/portall", messages.error(request, "El estudiante ya pertenece al curso"))

    try:
        usuario = User.objects.get(username=username)
    except:
        usuario = False

    if not usuario:
        return redirect("/portall", messages.error(request, "Ese estudiante no existe"))
    else:
        curso.cuentas.add(usuario)
        return redirect("/portall", messages.error(request, f"{usuario.username} agregado al curso {curso.nombre_curso}"))

def mensaje(request, id_persona):
    persona = User.objects.get(id=id_persona)

    context = {
        "persona": persona
    }

    return render(request, "PortAll50/persona.html", context)

def chatCurso(request, id_curso):
    curso = Curso.objects.get(id=id_curso)

    chat = Chat.objects.get(curso=curso)

    context = {
        "chat": chat
    }

    return render(request, "PortAll50/chatCurso.html", context)

def finalizarCurso(request):
    id_curso = request.POST.get("curso_id")

    curso = Curso.objects.get(id=id_curso)

    total_acumular = curso.total_acumular
    actual_acumulado = curso.actual_acumulado

    if actual_acumulado < total_acumular:
        return redirect(f"curso/{id_curso}", messages.error(request, "No se puede finalizar el curso porque no se ha alcanzado la nota a acumular total"))

    curso.estado_curso = "2"

    curso.save()

    return redirect(f"curso/{id_curso}")