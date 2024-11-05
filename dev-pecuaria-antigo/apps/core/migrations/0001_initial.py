# Generated by Django 4.2.7 on 2023-11-17 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Marca')),
                ('description', models.CharField(max_length=100, verbose_name='Descrição')),
            ],
            options={
                'verbose_name_plural': 'Marcas',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Categoria')),
                ('description', models.CharField(max_length=100, verbose_name='Descrição')),
            ],
            options={
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='InstituitionUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Unidade')),
                ('description', models.CharField(max_length=100, verbose_name='Descrição')),
            ],
            options={
                'verbose_name_plural': 'Unidades de Instituição',
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Instituição')),
                ('description', models.CharField(max_length=100, verbose_name='Descrição')),
            ],
            options={
                'verbose_name_plural': 'Instituições',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Fabricante')),
                ('description', models.CharField(max_length=100, verbose_name='Descrição')),
            ],
            options={
                'verbose_name_plural': 'Fabricantes',
            },
        ),
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Medida')),
                ('description', models.CharField(max_length=100, verbose_name='Descrição')),
            ],
            options={
                'verbose_name_plural': 'Medidas',
            },
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Modelo')),
                ('description', models.CharField(max_length=100, verbose_name='Descrição')),
            ],
            options={
                'verbose_name_plural': 'Modelos',
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Embalagem')),
                ('description', models.CharField(max_length=100, verbose_name='Descrição')),
            ],
            options={
                'verbose_name_plural': 'Embalagens',
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Setor')),
                ('description', models.CharField(max_length=100, verbose_name='Descrição')),
                ('instituitionUnit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.instituitionunit', verbose_name='Unidade')),
            ],
            options={
                'verbose_name_plural': 'Setores',
            },
        ),
        migrations.CreateModel(
            name='SubSector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Sub Setor')),
                ('description', models.CharField(max_length=100, verbose_name='Descrição')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.sector', verbose_name='Setor')),
            ],
            options={
                'verbose_name_plural': 'Sub Setores',
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Subcategoria')),
                ('description', models.CharField(max_length=100, verbose_name='Descrição')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.category')),
            ],
            options={
                'verbose_name_plural': 'Subcategorias',
            },
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('description', models.CharField(max_length=100, verbose_name='Descrição')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.brand', verbose_name='Marca')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.category', verbose_name='Categoria')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.manufacturer', verbose_name='Fabricante')),
                ('measure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.measure')),
                ('model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.model')),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.package')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.subcategory', verbose_name='Subcategoria')),
            ],
            options={
                'verbose_name_plural': 'Produtos',
            },
        ),
        migrations.AddField(
            model_name='instituitionunit',
            name='instituition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.institution', verbose_name='Instituição'),
        ),
    ]
