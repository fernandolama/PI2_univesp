# Generated by Django 5.0.6 on 2024-10-21 01:15

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_foto', '0005_recursoevento_tipoevento_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TamanhoFoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('medidas', models.CharField(max_length=20, unique=True)),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='pedidoimpressao',
            name='preco_unitario',
        ),
        migrations.AlterField(
            model_name='pedidoimpressao',
            name='tamanho_foto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to='app_foto.tamanhofoto'),
        ),
    ]
