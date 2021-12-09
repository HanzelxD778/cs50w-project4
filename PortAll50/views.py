from django.http import HttpResponse, request
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages #import messages
from django.contrib.auth.decorators import login_required
from . models import Cuenta, Curso, Entrega, Foro, Material, Entregable, RespuestaForo, Seccion
from datetime import datetime

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

    context = {
        "cursos": Curso.objects.all(),
        "usuario": Cuenta.objects.get(username=usuario)
    }

    return render(request, "portall50/portall.html", context)

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

    propietario = User.objects.filter(pk=propietario_curso)

    propietario = propietario[0]

    #el objeto creado primero
    curso = Curso.objects.create(nombre_curso=nombre_curso, propietario=propietario, imagen=txtImagen)

    for estudianteID in estudiantes_curso:
        estudiante = User.objects.get(pk=estudianteID)

        if estudiante:
            curso.cuentas.add(estudiante)

    curso.cuentas.add(propietario)

    return redirect("/portall")

def curso(request, id_curso):

    curso = Curso.objects.get(id=id_curso)
    #materiales = Material.objects.filter(seccion__curso=curso)
    #entregables = Entregable.objects.filter(seccion__curso=curso)
    #foros = Foro.objects.filter(seccion__curso=curso)

    context = {
        "curso": curso
        #"materiales": materiales,
        #"entregables": entregables,
        #"foros": foros
    }

    return render(request, "PortAll50/curso.html", context)

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

    seccion = Seccion.objects.get(pk=seccion_id)

    fecha_hora = f"{date}T{time}" 

    fecha = datetime.fromisoformat(fecha_hora)
    #datetime.fromisoformat('2011-11-04T00:05:23')

    entregable = Entregable.objects.create(nombre_entregable=nombre_entregable, archivo=archivo, comentario=comentario, tiempo_disp_hasta=fecha,seccion=seccion)

    return redirect(f"curso/{id_curso}")

def entregable(request, id_entregable):
    entregable = Entregable.objects.get(id=id_entregable)
    entregas = Entrega.objects.filter(entregable=entregable)

    context = {
        "entregable": entregable,
        "entregas": entregas
    }

    return render(request, "PortAll50/entregable.html", context)

def agregarEntrega(request):
    archivo_entrega = request.FILES.get("archivo_entrega")
    id_entregable = request.POST.get("id_entregable")
    id_cuenta = request.POST.get("id_cuenta")

    entregable = Entregable.objects.get(id=id_entregable)

    cuenta = User.objects.get(id=id_cuenta)

    agregarEntrega = Entrega.objects.create(archivo_entrega=archivo_entrega, entregable=entregable, cuenta=cuenta.info_cuenta)

    return redirect("/portall")

def agregarForo(request):
    nombre_foro = request.POST.get("nombre_foro")
    asignacion_foro = request.POST.get("asignacion_foro")
    date = request.POST.get("date")
    time = request.POST.get("time")
    seccion_id = request.POST.get("seccion_id")
    id_curso = request.POST.get("curso_id")

    seccion = Seccion.objects.get(pk=seccion_id)
    
    fecha_hora = f"{date}T{time}" 

    fecha = datetime.fromisoformat(fecha_hora)
    #datetime.fromisoformat('2011-11-04T00:05:23')

    foro = Foro.objects.create(nombre_foro=nombre_foro, asignacion_foro=asignacion_foro, fecha_vencimiento=fecha, seccion=seccion)

    return redirect(f"curso/{id_curso}")

def foro(request, id_foro):
    foro = Foro.objects.get(id=id_foro)
    respuestasForo = RespuestaForo.objects.filter(foro=foro)

    context = {
        "foro": foro,
        "respuestasForo": respuestasForo
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