from django.http import HttpResponse
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

    return HttpResponseRedirect(reverse("portall"))

def portall(request):

    propietario = request.user
    
    context = {
        "usuarios": User.objects.all(),
        "propietario": propietario,
        "cursos": Curso.objects.all(),
    }

    return render(request, "portall50/portall.html", context)

def registrarCurso(request):
    nombre_curso = request.POST.get("nombre_curso")
    estudiantes_curso = request.POST.get("estudiantes_curso")
    propietario_curso = request.POST.get("propietario_curso")

    user = User.objects.get(username=propietario_curso)

    curso = Curso.objects.create(nombre_curso=nombre_curso, propietario=user)

    return redirect("/portall")