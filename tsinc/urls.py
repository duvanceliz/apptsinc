from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home' ),
    path('createproject/', views.create_project, name='create_project'),
    path('createproduct/', views.create_product, name='create_product'),
    path('delete/<int:id>/', views.delete_project, name='delete_obj'),
    path('product/', views.product, name='product' ),
    path('dashboard/', views.dashboard, name='dashboard' ),
    path('uploadproducts/', views.upload_products, name='uploadproducts' ),
]
