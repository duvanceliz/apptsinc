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

