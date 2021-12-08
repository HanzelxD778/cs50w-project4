from django.http import HttpResponse, request
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages #import messages
from django.contrib.auth.decorators import login_required
from . models import Cuenta, Curso

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

    context = {
        "curso": Curso.objects.get(id=id_curso),
    }

    return render(request, "PortAll50/curso.html", context)