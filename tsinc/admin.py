from django.contrib import admin
from .models import Project, Brand, Location, Product, Units, Offers, Tabs, TabUnits, Slots
# Register your models here.


admin.site.register(Project)
admin.site.register(Brand)
admin.site.register(Location)
admin.site.register(Product)
admin.site.register(Units)
admin.site.register(Offers)
admin.site.register(Tabs)
admin.site.register(TabUnits)
admin.site.register(Slots)