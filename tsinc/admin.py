from django.contrib import admin
from .models import *
# Register your models here.

models_ = [ Project,
            Brand,
            Location,
            Product,
            Tabs,
            Dasboard,
            PanelItems,
            Items,
            Labels,
            Category,
            Subcategory,
            Folders,
            Sheet,
            Points,
            License,
            Divice,
            Total_points,
            Note,
            OfferCode,
            Remission,
            ProductSent,
            ProductBox,
            PurcharseOrder,
            OrderProduct,
            OrderEntry,
            ProductStatictics
           ]

admin.site.register(models_)
