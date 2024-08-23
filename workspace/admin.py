from django.contrib import admin
from .models import *
# Register your models here.

models_ = [Folder]
admin.site.register(models_)
