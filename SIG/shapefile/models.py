from django.contrib.gis.db import models


# Create your models here.
class Departamento(models.Model):
    cod_dep = models.CharField(80,primary_key=True)
    departamen = models.CharField(80)

    def __str__(self):
         return self.departamento

class Municipio(models.Model):
    cod_municipio = models.CharField(80,primary_key=True)
    municipio = models.CharField(80)
    zona = models.CharField(80)
    vereda = models.CharField(80)
    cod_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)


    def __str__(self):
        return self.municipio

    

class MinasPoint(models.Model):
        gid = models.AutoField(primary_key=True)
        cod_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
        cod_municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
        ano = models.CharField(80)
        mes = models.CharField(80)
        edad = models.CharField(80)
        ocupacion = models.CharField(80)
        genero = models.CharField(80)
        condicion = models.CharField(80)
        y = models.DecimalField(max_digits=20, decimal_places=10)
        x = models.DecimalField(max_digits=20, decimal_places=10)
        lugar_deto = models.CharField(80)
        actividad = models.CharField(80)
        y_cmt12 = models.CharField(80)
        x_cmt12 = models.CharField(80)
        geom = models.GeometryField(srid=4326)
        

        def __str__(self):
            return str(self.gid)

