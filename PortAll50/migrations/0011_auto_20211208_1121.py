# Generated by Django 3.2 on 2021-12-08 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PortAll50', '0010_alter_material_enlace'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entregable',
            name='tiempo_disp_desde',
        ),
        migrations.RemoveField(
            model_name='entregable',
            name='tiempo_disp_hasta',
        ),
        migrations.RemoveField(
            model_name='entregable',
            name='tiempo_ver_desde',
        ),
        migrations.RemoveField(
            model_name='entregable',
            name='tiempo_ver_para',
        ),
    ]
