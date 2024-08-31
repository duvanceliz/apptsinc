from django.db import models
import datetime
from django.contrib.auth.models import User 
import os
from django.core.validators import MaxLengthValidator
from django.utils import timezone

class Project(models.Model):
    name = models.CharField(max_length=200, default=None)
    company_name = models.CharField(max_length=200, default=None)
    nit = models.CharField(max_length=200,null=True)
    asesor = models.CharField(max_length=200, default=None)
    verified = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)
    date = models.DateField(default=datetime.date.today)
    usersession = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.name
    
class Brand(models.Model):
    product_brand = models.CharField(max_length=200, default=None)
    def __str__(self):
        return self.product_brand

class Location(models.Model):
    product_location = models.CharField(max_length=200, default=None)
    def __str__(self):
        return self.product_location

class Product(models.Model):
    code = models.CharField(max_length=200, default=None)
    product_name = models.CharField(max_length=200, default=None)
    factory_ref = models.CharField(max_length=200, default=None)
    model = models.CharField(max_length=200, default=None)
    sale_price = models.FloatField(default=0)
    sale_price_cop = models.FloatField(default=0)
    purcharse_price = models.FloatField(default=0)
    purcharse_price_cop = models.FloatField(default=0)
    brand = models.CharField(max_length=200, default=None)
    location = models.CharField(max_length=200, default=None)
    quantity = models.IntegerField()
    point = models.CharField(max_length=100,null=True,blank=True)
    observation =models.CharField(max_length=250, null=True)
    description = models.TextField(validators=[MaxLengthValidator(500)], null=True)
    min_stock = models.IntegerField(default=0)
    iva = models.BooleanField(default=False)
    date = models.DateField(default=datetime.date.today)
    def __str__(self):
        return f"{self.brand} - {self.model}"

    
class Tabs(models.Model):
    tab_name = models.CharField(max_length=200, default=None)
    controller = models.CharField(max_length=100, null=True)
    chest_type = models.BooleanField(default=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE, related_name='tabs', null=True, blank=True)
    def __str__(self):
        return self.tab_name
    

class Dasboard(models.Model):
    name = models.CharField(max_length=200, default=None)
    quantity = models.IntegerField(default=0)
    tab = models.ForeignKey(Tabs, on_delete=models.CASCADE, related_name='dashboards',null=True,blank=True)
    def __str__(self):
        return self.name
    
class Folders(models.Model):
    name = models.CharField(max_length=100, default=None)
    path = models.CharField(max_length=200,  default=None)
    def __str__(self):
        return self.name

class PanelItems(models.Model):
    name = models.CharField(max_length=100, null=True)
    img = models.CharField(max_length=100, default=None)
    tag = models.CharField(max_length=100,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='items', null=True, blank=True)
    folder = models.ForeignKey(Folders, on_delete=models.CASCADE, related_name='panelitems', null=True)
    def __str__(self):
        return self.img

class Items(models.Model):
    tag = models.CharField(max_length=200, null=True) 
    id_code = models.CharField(max_length=50, default=None)
    x = models.FloatField()
    y = models.FloatField()
    zindex = models.IntegerField(default=0)
    width = models.FloatField(default=0)
    height = models.FloatField(default=0)
    img = models.ForeignKey(PanelItems, on_delete=models.CASCADE, related_name='panelitem')
    relationship = models.CharField(max_length=50, null=True)
    dashboard = models.ForeignKey(Dasboard, on_delete=models.CASCADE, related_name='dashboard')
    def __str__(self):
        return self.id_code
    
class Labels(models.Model):
    id_code = models.CharField(max_length=50, default=None)
    value = models.CharField(max_length=200, default=None)
    x = models.FloatField()
    y = models.FloatField()
    zindex = models.IntegerField(default=0)
    width = models.FloatField(default=0)
    height = models.FloatField(default=0)
    relationship = models.CharField(max_length=50, null=True)
    dashboard = models.ForeignKey(Dasboard, on_delete=models.CASCADE, related_name='labels')
    def __str__(self):
        return self.id_code


class Category(models.Model):
    name= models.CharField(max_length=100, default=None)
    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=100, default=None)
    tag = models.CharField(max_length=100, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategory')
    def __str__(self):
        return self.name


class Sheet(models.Model):
    name = models.CharField(max_length=100, default=None)
    project = models.ForeignKey(Project,on_delete=models.CASCADE, related_name='sheet')
    def __str__(self):
        return self.name

class Points(models.Model):
    is_controller = models.BooleanField(default=False)
    name = models.CharField(max_length=100, default=None)
    eu = models.IntegerField(default=0)
    ed = models.IntegerField(default=0)
    sa = models.IntegerField(default=0)
    sd = models.IntegerField(default=0)
    sc = models.IntegerField(default=0)
    sheet = models.ForeignKey(Sheet,on_delete=models.CASCADE, related_name='point')
    def __str__(self):
        return self.name

class License(models.Model):
    name = models.CharField(max_length=100, default=None)
    description = models.CharField(max_length=200, default=None)
    sheet = models.ForeignKey(Sheet,on_delete=models.CASCADE, related_name='license', null=True)
    def __str__(self):
        return self.ref


class Divice(models.Model):
    tag = models.CharField(max_length=100, default=None, null=True) 
    model = models.CharField(max_length=100,default=None) 
    brand = models.CharField(max_length=100,default=None)
    tab = models.ForeignKey(Tabs,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.model
    
class Total_points(models.Model):
    sheet = models.CharField(max_length=100,default=None)
    total = models.IntegerField(default=0)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)

class Note(models.Model):
    tag = models.CharField(max_length=200)
    description = models.TextField(validators=[MaxLengthValidator(5000)]) 
    def __str__(self):
        return self.tag
    

class OfferCode(models.Model):
    name = models.CharField(max_length=100,null=True)
    code = models.CharField(max_length=100)
    def __str__(self):
        return self.code

class Remission(models.Model):
    number = models.CharField(max_length=200, null= True)
    city = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    nit = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    contruction_site= models.CharField(max_length=250, null=True)
    supplier = models.CharField(max_length=250, null=True)
    responsible = models.CharField(max_length=200)
    order_number = models.CharField(max_length=100, null=True) 
    observation = models.CharField(max_length=250, null=True) 
    date = models.DateTimeField(default=timezone.now)
    usersession = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True )
    project = models.ForeignKey(Project,on_delete=models.CASCADE, null=True, blank=True)

class ProductSent(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    remission = models.ForeignKey(Remission,on_delete=models.CASCADE,null=True)
    discounted = models.BooleanField(default=False)
    def __str__(self):
        return self.product.product_name
    
class ProductBox(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    usersession = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank=True)
    def __str__(self):
        return self.product.product_name

class PurcharseOrder(models.Model):
    code =  models.CharField(max_length=200)
    tracking =  models.CharField(max_length=250,null=True)
    supplier = models.CharField(max_length=200, null=True)
    nit = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    customer = models.CharField(max_length=200, null=True)
    cost_center = models.CharField(max_length=200, null=True)
    inspector = models.CharField(max_length=200, null=True)
    supervisor = models.CharField(max_length=200, null=True)
    paid = models.BooleanField(default=False)
    currency = models.BooleanField(default=False)
    observation = models.CharField(max_length=250, null=True) 
    total_price = models.FloatField(default=0)
    total_quantity = models.IntegerField(default=0)
    usersession = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    progress = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.code

class OrderProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    order = models.ForeignKey(PurcharseOrder,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.product.product_name

class OrderEntry(models.Model):
    order = models.ForeignKey(PurcharseOrder,on_delete=models.CASCADE)
    tracking = models.CharField(max_length=200, null=True)
    product = models.ForeignKey(OrderProduct,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    added = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

class ProductStatictics(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    rotations = models.IntegerField(default=0)
    out_stock = models.FloatField(default=0)

class Trm(models.Model):
    currency = models.CharField(max_length=50)
    value = models.FloatField(default=0)

class RemissionFile(models.Model):
    name = models.CharField(max_length=200)
    remission = models.ForeignKey(Remission,on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now)
    usersession = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank=True)

class OrderFile(models.Model):
    name = models.CharField(max_length=200)
    order = models.ForeignKey(PurcharseOrder,on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now)
    usersession = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank=True)

class ProductFile(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now)
    usersession = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank=True)

class Invoice(models.Model):
    number = models.CharField(max_length=100)
    total_price = models.FloatField(default=0)
    iva = models.FloatField(default=0)
    source_retention = models.FloatField(default=0)
    ica_retention = models.FloatField(default=0)
    usersession = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.number
    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"

class OrderInvoice(models.Model):
    order = models.ForeignKey(PurcharseOrder,on_delete=models.CASCADE, null=True)
    value_paid = models.FloatField(default=0)
    iva = models.FloatField(default=0)
    source_retention = models.FloatField(default=0)
    ica_retention = models.FloatField(default=0)
    usersession = models.ForeignKey(User,on_delete=models.SET_NULL,
                                     null=True)
    date = models.DateTimeField(default=timezone.now)


# class Folder(models.Model):
#     name = models.CharField(max_length=200)
#     parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
#     def __str__(self):
#         return self.name
#     class Meta:
#         verbose_name = "Carpeta"
#         verbose_name_plural = "Carpetas"


class Folder(models.Model):
    name = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=50, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    usersession = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True )
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Carpeta"
        verbose_name_plural = "Carpetas"
        ordering = ['order']