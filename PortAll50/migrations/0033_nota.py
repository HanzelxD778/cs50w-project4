# Generated by Django 3.2 on 2021-12-15 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PortAll50', '0032_delete_nota'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('curso', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='nota_curso', to='PortAll50.curso')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nota_estudiante', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Nota',
            },
        ),
    ]
