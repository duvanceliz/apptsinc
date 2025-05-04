from django import forms
from django.forms import formset_factory
from .models import Brand, Location, Tabs, Product, User, PanelItems
from django.db.models import Q
import datetime
from dal import autocomplete


class CreateProject(forms.Form):
    name = forms.CharField(label="Nombre del proyecto", 
                           max_length=200,
                           widget=forms.TextInput(attrs={'class': 'form-control'})
                           
                           )
    company_name = forms.CharField(label="Nombre de la empresa",
                                   max_length=200,
                                   widget=forms.TextInput(attrs={'class': 'form-control'})
                                   )
    nit = forms.CharField(label="NIT",
                          max_length=200,
                          widget=forms.TextInput(attrs={'class': 'form-control'})
                          )
    delivery_date = forms.DateField(label='Fecha de entrega',
                                    widget=forms.DateInput(attrs={'type': 'date','class':'form-control'}),
                                    initial=datetime.date.today
                                    )
    closing_date = forms.DateField(label='Fecha de cierre',
                                   widget=forms.DateInput(attrs={'type': 'date','class':'form-control'}),
                                   initial=datetime.date.today
                                   )
    OPCIONES_CHOICES = [
        ('Roberto Bravo', 'Roberto Bravo'),
        ('Erwin Serrano', 'Erwin Serrano'),
        ('Angela Ramirez', 'Angela Ramirez'),
        ('Catalina Pinilla', 'Catalina Pinilla'),

    ]
    asesor = forms.ChoiceField(label="Asesor",
                               choices=OPCIONES_CHOICES,
                              widget=forms.Select(attrs={'class': 'form-select'})
                               )
    # asesor = forms.ChoiceField(
    #     label="Asesor",
    #     choices=[(user.id, f"{user.username} {user.last_name}") for user in User.objects.all() if user.is_staff ],
    #     widget=forms.Select(attrs={'class': 'form-select'}),
    # )
    
class CreateTask(forms.Form):
    name = forms.CharField(label="Nombre de la tarea", 
                           max_length=250,
                           widget=forms.TextInput(attrs={'class': 'form-control'})
                           
                           )
    start_date = forms.DateField(label='Fecha de inicio',
                                 widget=forms.DateInput(attrs={'type': 'date','class':'form-control'}),
                                 initial=datetime.date.today
                                 )
    due_date = forms.DateField(label='Fecha proyectada de finalizacion',
                               widget=forms.DateInput(attrs={'type': 'date','class':'form-control'}),
                               initial=datetime.date.today

                               )
    description = forms.CharField(label="Descripción",max_length=500, widget=forms.Textarea(attrs={'class': 'form-control'}))
    send_email = forms.BooleanField(
        label="Enviar notificación al correo", 
        required=False, 
        initial=True
    )
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_staff=True),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
        
    )


class CreateProduct(forms.Form):
    code = forms.CharField(label="Codigo del Producto", max_length=200, 
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    product_name = forms.CharField(label="Nombre del Producto", max_length=200,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    ref = forms.CharField(label="Referencia de fabrica",max_length=200,
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    model = forms.CharField(label="Modelo",max_length=200,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    purcharse_price = forms.FloatField(label="Precio de compra",
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    sale_price = forms.FloatField(label="Precio de venta",
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    brand =  forms.CharField(label="Marca",max_length=200,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(label="Ubicacion",max_length=200,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(label="Cantidad",
                                    widget=forms.NumberInput(attrs={'class': 'form-control','min': '1'}),
                                    min_value=1)

    point = forms.CharField(label="Puntos del dipositivo",max_length=200,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    min_stock = forms.IntegerField(label="Stock Minimo",
                                    widget=forms.NumberInput(attrs={'class': 'form-control','min': '1'}),
                                    min_value=1
                                    )
    
    observation = forms.CharField(label="Observación",max_length=200,
                                    widget=forms.TextInput(attrs={'class': 'form-control'})
                                    )

    description = forms.CharField(label="Descripción",max_length=500, widget=forms.Textarea(attrs={'class': 'form-control'}))

    iva = forms.BooleanField(label="Tiene el IVA incluido?")

class UploadProducts(forms.Form):
    file = forms.FileField()
    original = forms.BooleanField(required=False)

class CreateTab(forms.Form):
    tab_name = forms.CharField(label="Nombre del tablero", 
                               max_length=200,
                               widget=forms.TextInput(attrs={'class': 'form-control','value':'TAB CONT 01'})

                               )
    OPCIONS_CHOICES_TAB = [
        (1, 'TABLERO CONTROLADOR'),
        (2, 'TABLERO SUPERVISOR'),
        
    ]
    OPCIONS_CHOICES_CONTROLLER = [
        ('LG BECON CONTROLLER', 'LG BECON CONTROLLER'),
        ('JCI FACILITY EXPLORER', 'JCI FACILITY EXPLORER'),
        ('JCI METASYS', 'JCI METASYS'),
        
    ]

    chest_type = forms.ChoiceField(label="Tipo de Tablero", 
                                   choices=OPCIONS_CHOICES_TAB,
                                     widget=forms.Select(attrs={'class': 'form-select'})
                                   )

    controller = forms.ChoiceField(label="Elige el fabricante", 
                                   choices=OPCIONS_CHOICES_CONTROLLER,
                                     widget=forms.Select(attrs={'class': 'form-select'})
                                   )
    

class CreatePage(forms.Form):
    name = forms.CharField(label="Nombre de página", 
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control','value':'pag-1'})

                           )

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

class CreateRemission(forms.Form):
    order_number = forms.CharField(label="Pedido No.", 
                                  max_length=100,
                                   widget=forms.TextInput(attrs={'class': 'form-control'})
                                  
                                  )
    city = forms.CharField(label="Ciudad", 
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control'})
                           
                           )
    company = forms.CharField(label="Razon Social", 
                              max_length=100,
                              widget=forms.TextInput(attrs={'class': 'form-control'})
                              )
    nit = forms.CharField(label="NIT", 
                          max_length=100,
                          widget=forms.TextInput(attrs={'class': 'form-control'})
                          )
    location = forms.CharField(label="Lugar de entrega", 
                               max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'})
                               )
    project = forms.CharField(label="Obra",
                               max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control'})
                               )
    responsible = forms.CharField(label="Ingeniero responsable", 
                                  max_length=100,
                                   widget=forms.TextInput(attrs={'class': 'form-control'})
                                  
                                  )
    observation = forms.CharField(label="Observación", 
                                  max_length=250,
                                   widget=forms.TextInput(attrs={'class': 'form-control'})
                                  
                                  )

   

class CreateOrder(forms.Form):
    tracking = forms.CharField(label="Tracking", 
                           max_length=250,
                           widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    supplier = forms.CharField(label="Proveedor/contratista", 
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nit = forms.CharField(label="NIT", 
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(label="Dirección", 
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(label="Telefono", 
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    customer = forms.CharField(label="Cliente", 
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    cost_center = forms.CharField(label="Centro de costo", 
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    inspector = forms.CharField(label="Interventor", 
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    supervisor = forms.CharField(label="Supervisor", 
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    observation = forms.CharField(label="Observacion", 
                           max_length=250,
                           widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    currency = forms.BooleanField(
        label="Está en COP?",
        widget=forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
        required=False,
        initial=False  # Establece "No" como valor predeterminado
    )

class UploadFile(forms.Form):
    file = forms.FileField() 

class CreateInvoice(forms.Form):
    number = forms.CharField(label="numero de factura", 
                           max_length=250,
                           widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    total_price = forms.FloatField(label="Precio total",
                                    widget=forms.NumberInput(attrs={'class': 'form-control','min': '1'}),
                                    min_value=1
                                    )
    iva = forms.FloatField(label="Valor de IVA",
                                    widget=forms.NumberInput(attrs={'class': 'form-control','min': '1'}),
                                    min_value=1
                                    )
    source_retention = forms.FloatField(label="Retención en la fuente",
                                    widget=forms.NumberInput(attrs={'class': 'form-control','min': '1'}),
                                    min_value=1
                                    )
    ica_retention = forms.FloatField(label="Retención ICA",
                                    widget=forms.NumberInput(attrs={'class': 'form-control','min': '1'}),
                                    min_value=1
                                    )
 

class PanelItemsForm(forms.ModelForm):
    class Meta:
        model = PanelItems
        fields = '__all__'
        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete')
        }



