# Generated by Django 3.2 on 2021-12-11 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PortAll50', '0023_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='url',
            old_name='curso',
            new_name='seccion',
        ),
    ]
