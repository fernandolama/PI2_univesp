# Generated by Django 5.0.6 on 2024-10-27 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_foto', '0009_alter_telefone_codigo_area_alter_telefone_numero'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='data_nascimento',
        ),
    ]
