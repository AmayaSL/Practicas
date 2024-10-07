# Generated by Django 5.1.1 on 2024-10-01 15:09

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('cod_departamento', models.IntegerField(primary_key=True, serialize=False)),
                ('departamento', models.CharField(verbose_name=100)),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('cod_municipio', models.IntegerField(primary_key=True, serialize=False)),
                ('municipio', models.CharField(verbose_name=100)),
                ('zona', models.CharField(verbose_name=100)),
                ('vereda', models.CharField(verbose_name=255)),
                ('cod_departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shapefile.departamento')),
            ],
        ),
        migrations.CreateModel(
            name='MinasPoint',
            fields=[
                ('gid', models.AutoField(primary_key=True, serialize=False)),
                ('ano', models.PositiveIntegerField()),
                ('mes', models.PositiveIntegerField()),
                ('edad', models.PositiveIntegerField()),
                ('ocupacion', models.CharField(verbose_name=255)),
                ('genero', models.CharField(verbose_name=50)),
                ('condicion', models.CharField(verbose_name=100)),
                ('y', models.FloatField()),
                ('x', models.FloatField()),
                ('lugar_deto', models.CharField(verbose_name=150)),
                ('actividad', models.CharField(verbose_name=150)),
                ('y_cmt12', models.FloatField()),
                ('x_cmt12', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
                ('cod_departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shapefile.departamento')),
                ('cod_municipio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shapefile.municipio')),
            ],
        ),
    ]
