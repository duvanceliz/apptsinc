from django.db import models
import datetime
from django.contrib.auth.models import User 
import os
from django.core.validators import MaxLengthValidator

class Project(models.Model):
    name = models.CharField(max_length=200, default=None)
    company_name = models.CharField(max_length=200, default=None)
    nit = models.CharField(max_length=200,null=True)
    asesor = models.CharField(max_length=200, default=None)
    verified = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)
    date = models.DateField(default=datetime.date.today)
    usersesion = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
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
    brand = models.CharField(max_length=200, default=None)
    location = models.CharField(max_length=200, default=None)
    quantity = models.IntegerField()
    point = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(validators=[MaxLengthValidator(500)], null=True) 
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
    code = models.CharField(max_length=100)
    def __str__(self):
        return self.code
    
