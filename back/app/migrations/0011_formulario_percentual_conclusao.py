# Generated by Django 5.1.6 on 2025-02-21 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rename_data_formulario_data_criacao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulario',
            name='percentual_conclusao',
            field=models.FloatField(default=0.0),
        ),
    ]
