# Generated by Django 3.2 on 2021-12-10 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PortAll50', '0021_alter_entrega_cuenta'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrega',
            name='estado_entrega',
            field=models.CharField(choices=[('0', 'No enviada'), ('1', 'Enviada')], default='0', max_length=1),
        ),
    ]
