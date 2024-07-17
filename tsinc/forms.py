from django import forms
from django.forms import formset_factory
from .models import Brand, Location, Tabs, Product
from django.db.models import Q


class CreateProject(forms.Form):
    name = forms.CharField(label="Nombre del proyecto", max_length=200)
    company_name = forms.CharField(label="Nombre de la empresa",max_length=200)
    nit = forms.CharField(label="NIT",max_length=200)
    OPCIONES_CHOICES = [
        ('Roberto Bravo', 'Roberto Bravo'),
        ('Edwin Serrano', 'Edwin Serrano'),
        ('Angela Ramirez', 'Angela Ramirez'),
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
    original = forms.BooleanField(required=False)

class CreateTab(forms.Form):
    tab_name = forms.CharField(label="Nombre del tablero", max_length=200)
    OPCIONS_CHOICES_TAB = [
        (1, 'TABLERO CONTROLADOR'),
        (2, 'TABLERO SUPERVISOR'),
        
    ]
    OPCIONS_CHOICES_CONTROLLER = [
        ('LG BECON CONTROLLER', 'LG BECON CONTROLLER'),
        ('JCI FACILITY EXPLORER', 'JCI FACILITY EXPLORER'),
        ('JCI METASYS', 'JCI METASYS'),
        
    ]

    chest_type = forms.ChoiceField(label="Tipo de Tablero", choices=OPCIONS_CHOICES_TAB)

    controller = forms.ChoiceField(label="Elige el fabricante", choices=OPCIONS_CHOICES_CONTROLLER)
    

class CreatePage(forms.Form):
    name = forms.CharField(label="Nombre de página", max_length=100)

class SearchForm(forms.Form):
    search = forms.CharField(label='Buscar', max_length=100)

class UploadSVGForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}), label='Select multiple files')

# class CreateOffer(forms.Form):
#     title = forms.CharField(label="Nombre del proyecto", max_length=200)
#     OPCIONES_CHOICES = [
#         ('JONHSON CONTROLS', 'JONHSON CONTROLS'),
#         ('LG CONTROLLER', 'LG CONTROLLER')
#     ]
#     controller = forms.ChoiceField(choices=OPCIONES_CHOICES)

class AddController(forms.Form):
    controller = forms.ModelChoiceField(label="Elige un modulo",queryset=Product.objects.filter(Q(code__icontains="C-FE") | Q(code__icontains="E-FE") | Q(code__icontains="C-LG") | Q(code__icontains="E-LG") | Q(code__icontains="SV")))

class AddLicense(forms.Form):
    license = forms.ModelChoiceField(label="licencias",queryset=Product.objects.filter(product_name__icontains="LICENCIA"))