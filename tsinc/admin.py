from django.contrib import admin
from .models import Project, Brand, Location, Product
# Register your models here.


admin.site.register(Project)
admin.site.register(Brand)
admin.site.register(Location)
admin.site.register(Product)