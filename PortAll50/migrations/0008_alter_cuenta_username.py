# Generated by Django 3.2 on 2021-12-07 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PortAll50', '0007_curso_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuenta',
            name='username',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='info_cuenta', to=settings.AUTH_USER_MODEL),
        ),
    ]