from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home' ),
    path('createproject/', views.create_project, name='create_project'),
    path('createproduct/', views.create_product, name='create_product'),
    path('delete/<int:id>/', views.delete_project, name='delete_obj'),
    path('product/', views.product, name='product' ),
    path('dashboard/<int:id>/', views.dashboard, name='dashboard' ),
    path('uploadproducts/', views.upload_products, name='uploadproducts' ),
    path('offer/', views.offer, name='offer'),
    path('offer/tabs/<int:id>/', views.tabs, name='tabs'),
    path('offer/tabs/units/<int:id>/', views.units, name='units'),
    path('offer/tabs/units/configuration/<int:id>/', views.config, name='config' ),
    path('deleteslot/<int:id>/', views.delete_slot, name='delete_slot'),
    path('deleteunit/<int:id>/', views.delete_unit, name='delete_unit'),
    path('deletetab/<int:id>/', views.delete_tab, name='delete_tab'),
    path('deleteoffer/<int:id>/', views.delete_offer, name='delete_offer'),
    path('downloadoffer/<int:id>/', views.download_offer, name='download_offer'),
    path('saveitems/', views.save_items, name='save_items'),
]
