from django.contrib import admin
from .models import *
# Register your models here.
from .forms import PanelItemsForm

@admin.register(PanelItems)
class PanelItemsAdmin(admin.ModelAdmin):
    form = PanelItemsForm

models_ = [ Project,
            Brand,
            Location,
            Product,
            Tabs,
            Dasboard,

            Items,
            Labels,
            Category,
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
            ProductStatictics,
            Trm,
            RemissionFile,
            OrderFile,
            ProductFile,
            Invoice,
            OrderInvoice,
            Folder,
            File,
            GeneratedOffer,
            Task,
            Activity,
            Comment
           ]
admin.site.register(models_)
