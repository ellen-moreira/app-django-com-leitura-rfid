# Generated by Django 5.0.7 on 2024-11-05 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_lote_observacao_alter_animal_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='animais/', verbose_name='Foto'),
        ),
    ]
