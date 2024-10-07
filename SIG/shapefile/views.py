from django.shortcuts import render, get_object_or_404, redirect
from shapefile.forms import DepartamentoForm, MunicipioForm, MinasPointForm
from django.contrib.gis.geos import Point
from shapefile.models import MinasPoint
from django.http import JsonResponse
from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework import status
import shapefile
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
import os
import geopandas as gpd
import tempfile

# Create your views here.



def verMapa(request):
    # Obtener los puntos y serializarlos a GeoJSON
    puntos = MinasPoint.objects.all()
    geojson_data = serialize('geojson', puntos, geometry_field='geom', fields=('ocupacion', 'genero', 'lugar_deto'))

    # Verifica si la solicitud es AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(geojson_data, safe=False)

    # Si no es AJAX, renderiza la plantilla HTML
    return render(request, 'gis/mapa.html', {'geojson_data': geojson_data})

def nuevoDepartamento(request):
    if request.method == 'POST':
        formaDepartamento = DepartamentoForm(request.POST)
        if formaDepartamento.is_valid():
            formaDepartamento.save()
            return redirect('inicio')
    else:
        formaDepartamento = DepartamentoForm()

    return render(request, 'departamentos/agregar_departamento.html' , {'formaDepartamento': formaDepartamento})

def nuevoMunicipio(request):
    if request.method == 'POST':
        formaMunicipio = MunicipioForm(request.POST)
        if formaMunicipio.is_valid():
            formaMunicipio.save()
            return redirect('inicio')
    else:
        formaMunicipio = MunicipioForm()

    return render(request, 'municipios/agregar_municipio.html' , {'formaMunicipio': formaMunicipio})



def nuevoMinasPoint(request):
    if request.method == 'POST':
        formaMinasPoint = MinasPointForm(request.POST)
        if formaMinasPoint.is_valid():
            # Obtener las coordenadas de X y Y
            x = formaMinasPoint.cleaned_data['x']
            y = formaMinasPoint.cleaned_data['y']
            point = Point(x, y, srid=4326)  # Crea un objeto Point con las coordenadas

            # Guardar la instancia de MinasPoint
            mina = formaMinasPoint.save(commit=False)
            mina.geom = point  # Asigna el objeto Point al campo geom
            mina.save()

            return redirect('inicio')  # Redirige a la vista de inicio
    else:
        formaMinasPoint = MinasPointForm()

    return render(request, 'minas/agregar_puntoMina.html', {'formaMinasPoint': formaMinasPoint})



def cargarArchivoVista(request):
    return render(request, 'archivo/cargar_archivo.html')  # Aquí tu plantilla que contiene el formulario



@api_view(['POST'])
def cargarArchivo(request):
    shapefile_shp = request.FILES.get('shapefile_shp')
    shapefile_shx = request.FILES.get('shapefile_shx')

    if not (shapefile_shp or shapefile_shx):
        return Response({'error': 'No se ha proporcionado ningún archivo .shp o .shx'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Crear un directorio temporal
        with tempfile.TemporaryDirectory() as temp_dir:
            # Guardar el archivo .shp en el directorio temporal
            shp_path = os.path.join(temp_dir, 'temp_shapefile.shp')
            with open(shp_path, 'wb') as f:
                for chunk in shapefile_shp.chunks():
                    f.write(chunk)

            # Confirmar que el archivo .shp se ha guardado
            if not os.path.exists(shp_path):
                return Response({'error': 'El archivo .shp no se guardó correctamente'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Verificar si hay un archivo .shx correspondiente
            shx_path = os.path.join(temp_dir, 'temp_shapefile.shx')
            with open(shx_path, 'wb') as f:
                for chunk in shapefile_shx.chunks():
                    f.write(chunk)
                    
            if not os.path.exists(shx_path):
                return Response({'error': 'El archivo .shx no se encontró'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Leer el shapefile usando GeoPandas
            gdf = gpd.read_file(shp_path)

            # Procesar cada geometría en el shapefile y guardarla en la base de datos
            for _, row in gdf.iterrows():
                geom = row.geometry
                if geom.geom_type == 'Point':  # Solo manejar puntos por ahora
                    point = Point(geom.x, geom.y)
                    MinasPoint.objects.create(geom=point)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'Archivos cargados correctamente'}, status=status.HTTP_201_CREATED)