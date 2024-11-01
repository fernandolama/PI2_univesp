# Generated by Django 5.0.6 on 2024-10-31 02:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_foto', '0012_alter_recursoevento_nome_alter_recursoevento_preco_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orcamentoevento',
            name='local_evento',
        ),
        migrations.AddField(
            model_name='endereco',
            name='local_evento',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='endereco_evento', to='app_foto.orcamentoevento'),
        ),
    ]
