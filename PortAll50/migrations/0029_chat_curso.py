# Generated by Django 3.2 on 2021-12-14 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PortAll50', '0028_remove_chat_curso'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='curso',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='chat', to='PortAll50.curso'),
            preserve_default=False,
        ),
    ]
