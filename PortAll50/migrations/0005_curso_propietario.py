# Generated by Django 3.2 on 2021-12-07 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PortAll50', '0004_remove_curso_propietario'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='propietario',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
