# Generated by Django 3.2 on 2021-12-08 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PortAll50', '0009_alter_curso_cuentas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='enlace',
            field=models.URLField(null=True),
        ),
    ]