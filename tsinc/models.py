from django.db import models
import datetime


class Project(models.Model):
    name = models.CharField(max_length=200, default=None)
    dibujante = models.CharField(max_length=200, default=None)
    approved = models.CharField(max_length=200, default=None)
    verified = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    date = models.DateField(default=datetime.date.today)
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
    iva = models.BooleanField(default=False)
    date = models.DateField(default=datetime.date.today)
    def __str__(self):
        return self.product_name

class Units(models.Model):
    name = models.CharField(max_length=200, default=None)
    description = models.CharField(max_length=200, default=None)
    def __str__(self):
        return self.name
class Offers(models.Model):
    title = models.CharField(max_length=200, default=None)
    controller = models.CharField(max_length=200, default=None)
    date = models.DateField(default=datetime.date.today)
    def __str__(self):
        return self.title
    
class Tabs(models.Model):
    tab_name = models.CharField(max_length=200, default=None)
    offer = models.ForeignKey(Offers,on_delete=models.CASCADE, related_name='tabs')
    def __str__(self):
        return self.tab_name
    
class TabUnits(models.Model):
    unit = models.CharField(max_length=200, default=None)
    quantity = models.IntegerField()
    tab = models.ForeignKey(Tabs,on_delete=models.CASCADE, related_name='units')
    def __str__(self):
        return self.unit

class Slots(models.Model):
    slot = models.CharField(max_length=255, null=True, blank=True)
    unit = models.ForeignKey(TabUnits,on_delete=models.CASCADE, related_name='slots')
    def __str__(self):
        return self.slot




