from django.contrib import admin

# Register your models here.
from django.contrib import admin
from shapefile.models import Departamento, Municipio, MinasPoint

admin.site.register(Departamento)
admin.site.register(Municipio)
admin.site.register(MinasPoint)
