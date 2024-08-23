from django.urls import path
from . import views

urlpatterns = [
    path('overview/', views.overview, name='overview'),
    path('folder/<str:name>/', views.overview_folder, name='overview_folder'),
]