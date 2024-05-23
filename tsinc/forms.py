from django import forms


class CreateProject(forms.Form):
    name = forms.CharField(label="Nombre del proyecto", max_length=200)
    dibujante = forms.CharField(label="Nombre del dibujante",max_length=200)
    dibujante = forms.CharField(label="Nombre del dibujante",max_length=200)
    OPCIONES_CHOICES = [
        ('Roberto Bravo', 'Roberto Bravo'),
        ('Andres Montoya', 'Andres Montoya'),
        ('Julian Alvarado', 'Julian Alvarado'),
    ]

    approved = forms.ChoiceField(choices=OPCIONES_CHOICES)


class CreateProduct(forms.Form):
    code = forms.CharField(label="Codigo del Producto", max_length=200)
    product_name = forms.CharField(label="Nombre del Producto", max_length=200)
    ref = forms.CharField(label="Referencia de fabrica",max_length=200)
    model = forms.CharField(label="Modelo",max_length=200)
    price = forms.FloatField(label="Precio de venta")
    iva = forms.BooleanField(label="Tiene el IVA incluido?")

class UploadProducts(forms.Form):
    file = forms.FileField()
