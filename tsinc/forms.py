from django import forms
from django.forms import formset_factory
from .models import Brand, Location, Tabs


class CreateProject(forms.Form):
    name = forms.CharField(label="Nombre del proyecto", max_length=200)
    company_name = forms.CharField(label="Nombre de la empresa",max_length=200)
    OPCIONES_CHOICES = [
        ('Roberto Bravo', 'Roberto Bravo'),
        ('Andres Montoya', 'Andres Montoya'),
        ('Julian Alvarado', 'Julian Alvarado'),
    ]
    asesor = forms.ChoiceField(label="Asesor",choices=OPCIONES_CHOICES)
  

class CreateProduct(forms.Form):
    code = forms.CharField(label="Codigo del Producto", max_length=200)
    product_name = forms.CharField(label="Nombre del Producto", max_length=200)
    ref = forms.CharField(label="Referencia de fabrica",max_length=200)
    model = forms.CharField(label="Modelo",max_length=200)
    price = forms.FloatField(label="Precio de venta")
    brand =  forms.ModelChoiceField(label="Marca",queryset=Brand.objects.all())
    location = forms.ModelChoiceField(label="Ubicacion",queryset=Location.objects.all())
    quantity = forms.IntegerField(label="Cantidad")
    iva = forms.BooleanField(label="Tiene el IVA incluido?")

class UploadProducts(forms.Form):
    file = forms.FileField()

class CreateTab(forms.Form):
    tab_name = forms.CharField(label="Nombre del tablero", max_length=200)
    OPCIONS_CHOICES_CONTROLLER = [
        ('LG CONTROLLER', 'LG CONTROLLER'),
        ('JONHSON CONTROLS', 'JONHSON CONTROLS'),
        
    ]

    controller = forms.ChoiceField(label="Elige el controlador", choices=OPCIONS_CHOICES_CONTROLLER)
    

class CreatePage(forms.Form):
    name = forms.CharField(label="Nombre de pagina", max_length=100)

class SearchForm(forms.Form):
    search = forms.CharField(label='Buscar', max_length=100)

# class CreateOffer(forms.Form):
#     title = forms.CharField(label="Nombre del proyecto", max_length=200)
#     OPCIONES_CHOICES = [
#         ('JONHSON CONTROLS', 'JONHSON CONTROLS'),
#         ('LG CONTROLLER', 'LG CONTROLLER')
#     ]
#     controller = forms.ChoiceField(choices=OPCIONES_CHOICES)