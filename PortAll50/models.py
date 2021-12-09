from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.related import ManyToManyField

# Create your models here.
class Cuenta(models.Model):
    username = models.OneToOneField(User, on_delete=CASCADE, related_name="info_cuenta")
    TIPO = [("1", "Estudiante"), ("2", "Docente")]
    tipo = models.CharField(max_length=1 ,choices=TIPO, default=1)
    imagen = models.ImageField(upload_to='users/', null = True) #investigar upload_to

    class Meta:
        verbose_name_plural = "Cuenta"

    def __str__(self):
        return f"{self.username} {self.tipo} {self.imagen}"

class Curso(models.Model):
    nombre_curso = models.CharField(max_length=60)
    cuentas = models.ManyToManyField(User, related_name="cursos_inscritos", null=True) #identifica participantes 
    propietario = models.ForeignKey(User, on_delete=CASCADE, related_name="cursos_creados")
    imagen = models.ImageField(upload_to='cursos/', null = True) #investigar upload_to

    class Meta:
        verbose_name_plural = "Curso"

    def __str__(self):
        return f"{self.nombre_curso} {self.cuentas} {self.propietario}"

class Seccion(models.Model):
    nombre = models.CharField(max_length=60)
    curso = models.ForeignKey(Curso, on_delete=CASCADE, related_name="seccion_curso")

    class Meta:
        verbose_name_plural = "Seccion"

    def __str__(self):
        return f"{self.nombre} {self.curso}"

class Material(models.Model):
    nombre_material = models.CharField(max_length=60)
    archivo = models.FileField(upload_to='materiales/', blank=True) #ver video axel
    #curso = models.ForeignKey(Curso, on_delete=CASCADE, related_name="materiales")
    seccion = models.ForeignKey(Seccion, on_delete=CASCADE, related_name="seccion_material")

    class Meta:
        verbose_name_plural = "Material"

    def __str__(self):
        return f"{self.nombre_material} {self.archivo} {self.seccion}"

class Enlace(models.Model):
    nombre_enlace = models.CharField(max_length=60)
    enlace = models.URLField()
    seccion = models.ForeignKey(Seccion, on_delete=CASCADE, related_name="seccion_enlace")

    class Meta:
        verbose_name_plural = "Enlace"

    def __str__(self):
        return f"{self.nombre_enlace} {self.enlace} {self.seccion}"

class Foro(models.Model):
    nombre_foro = models.CharField(max_length=60)
    asignacion_foro = models.CharField(max_length=300)
    fecha_vencimiento = models.DateTimeField() #investigar
    #curso = models.ForeignKey(Curso, on_delete=CASCADE, related_name="foros")
    seccion = models.ForeignKey(Seccion, on_delete=CASCADE, related_name="seccion_foro")

    class Meta:
        verbose_name_plural = "Foro"

    def __str__(self):
        return f"{self.nombre_foro} {self.asignacion_foro} {self.fecha_vencimiento} {self.seccion}"

class RespuestaForo(models.Model):
    respuesa_foro = models.CharField(max_length=1000)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)
    nota = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    foro = models.ForeignKey(Foro, on_delete=CASCADE, related_name="respuestas")
    cuenta = models.ForeignKey(Cuenta, on_delete=CASCADE, related_name="respuestas")

    class Meta:
        verbose_name_plural = "RespuestasForo"

    def __str__(self):
        return f"{self.respuesa_foro} {self.fecha_respuesta} {self.nota} {self.foro} {self.cuenta}"

class Chat(models.Model):
    nombre_chat = models.CharField(max_length=60)
    curso = models.ForeignKey(Curso, on_delete=CASCADE, related_name="chats")

    class Meta:
        verbose_name_plural = "Chat"

    def __str__(self):
        return f"{self.nombre_chat} {self.curso}"

class Mensaje(models.Model):
    mensaje = models.CharField(max_length=100)
    tiempo = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=CASCADE, related_name="mensajes")
    cuenta = models.ForeignKey(Cuenta, on_delete=CASCADE, related_name="mensajes")

    class Meta:
        verbose_name_plural = "Mensajes"

    def __str__(self):
        return f"{self.mensaje} {self.tiempo} {self.chat} {self.cuenta}"

class Entregable(models.Model):
    nombre_entregable = models.CharField(max_length=30)
    archivo = models.FileField(upload_to='entregables/', blank=True) #ver video axel
    comentario = models.CharField(max_length=100)
    tiempo_disp_hasta = models.DateTimeField(null=True)
    ESTADO_ENTREGA = [("1", "Mostrar"), ("2", "Recibida")]
    estado_entrega = models.CharField(choices=ESTADO_ENTREGA, max_length=1, default="1")
    #curso = models.ForeignKey(Curso, on_delete=CASCADE, related_name="entregables")
    seccion = models.ForeignKey(Seccion, on_delete=CASCADE, related_name="seccion_entregable")
    nota = models.DecimalField(decimal_places=2, max_digits=5, null=True)

    class Meta:
        verbose_name_plural = "Entregable"

    def __str__(self):
        return f"{self.nombre_entregable} {self.archivo} {self.comentario} {self.estado_entrega} {self.seccion} {self.nota}"

class Entrega(models.Model):
    archivo_entrega = models.FileField(upload_to="entregas/%Y/%m/%d", blank=True) #ver video axel
    tiempo_entregado = models.DateTimeField(auto_now_add=True)
    nota = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    entregable = models.ForeignKey(Entregable, on_delete=CASCADE, related_name="entregas")
    cuenta = models.ForeignKey(Cuenta, on_delete=CASCADE, related_name="entregas")

    class Meta:
        verbose_name_plural = "Entrega"

    def __str__(self):
        return f"{self.archivo_entrega} {self.tiempo_entregado} {self.nota} {self.entregable} {self.cuenta}"

##########################################################################################
#                                  HACER CUESTIONARIO
##########################################################################################
