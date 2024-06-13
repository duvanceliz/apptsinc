from django.db import models
import datetime
from django.contrib.auth.models import User 

class Project(models.Model):
    name = models.CharField(max_length=200, default=None)
    company_name = models.CharField(max_length=200, default=None)
    asesor = models.CharField(max_length=200, default=None)
    controller = models.CharField(max_length=100, null=True, blank=True)
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
    sale_price = models.FloatField()
    brand = models.CharField(max_length=200, default=None)
    location = models.CharField(max_length=200, default=None)
    quantity = models.IntegerField()
    point = models.CharField(max_length=100,null=True,blank=True)
    description = models.CharField(max_length=200,null=True,blank=True)
    iva = models.BooleanField(default=False)
    date = models.DateField(default=datetime.date.today)
    def __str__(self):
        return f"{self.brand} - {self.model}"

    
class Tabs(models.Model):
    tab_name = models.CharField(max_length=200, default=None)
    controller = models.CharField(max_length=100, null=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE, related_name='tabs', null=True, blank=True)
    def __str__(self):
        return self.tab_name
    

class Dasboard(models.Model):
    name = models.CharField(max_length=200, default=None)
    quantity = models.IntegerField(default=0)
    tab = models.ForeignKey(Tabs, on_delete=models.CASCADE, related_name='dashboards',null=True,blank=True)
    def __str__(self):
        return self.name

class PanelItems(models.Model):
    img = models.CharField(max_length=100, default=None)
    width = models.IntegerField()
    tag = models.CharField(max_length=100,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    def __str__(self):
        return self.img

class Items(models.Model):
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
    dashboard = models.ForeignKey(Dasboard, on_delete=models.CASCADE, related_name='labels')
    def __str__(self):
        return self.id_code


