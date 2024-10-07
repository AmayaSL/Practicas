from django.forms import ModelForm, EmailInput, TextInput, NumberInput
from shapefile.models import Departamento, Municipio, MinasPoint
from django import forms
from django.contrib.gis.geos import Point

class DepartamentoForm(ModelForm):
    class Meta:
        model = Departamento
        fields = '__all__'

class MunicipioForm(ModelForm):
    class Meta:
        model = Municipio
        fields = '__all__'
        widgets = {
            'cod_municipio': TextInput(attrs={'type': 'number'})
        }


class MinasPointForm(forms.ModelForm):
    class Meta:
        model = MinasPoint
        fields = [ 'cod_departamento','cod_municipio', 'ano', 'mes', 'edad', 'ocupacion', 
                  'genero', 'condicion', 'y', 'x', 'lugar_deto', 
                  'actividad','y_cmt12','x_cmt12']  # Sin geom
        widgets = {
            'ano': forms.NumberInput(attrs={'type': 'number'}),
            'mes': forms.NumberInput(attrs={'type': 'number', 'step': '1'}),
            'edad': forms.NumberInput(attrs={'type': 'number', 'step': '1'}),
            'ocupacion': forms.TextInput(attrs={'type': 'text'}),
            'genero': forms.TextInput(attrs={'type': 'text'}),
            'condicion': forms.TextInput(attrs={'type': 'text'}),
            'y': forms.NumberInput(attrs={'type': 'number'}),
            'x': forms.NumberInput(attrs={'type': 'number'}),
            'actividad': forms.TextInput(attrs={'type': 'text'}),
            'y_cmt12': forms.NumberInput(attrs={'type': 'number'}),
            'x_cmt12': forms.NumberInput(attrs={'type': 'number'}),
            
        }
