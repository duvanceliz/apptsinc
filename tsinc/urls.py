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
    path('project/tabs/<int:id>/', views.tabs, name='tabs'),
    path('deletetab/<int:id>/', views.delete_tab, name='delete_tab'),
    path('deletepage/<int:id>/', views.delete_page, name='delete_page'),
    path('downloadoffer/<int:id>/', views.download_offer, name='download_offer'),
    path('saveitems/', views.save_items, name='save_items'),
    path('createpage/<int:id>/', views.create_page, name='create_page'),
    path('deleteitem/', views.delete_item, name='delete_item'),
    path('productsearch/', views.product_search, name='product_search'),
    path('totalproducts/', views.total, name='total'),
    path('downloadproducts/', views.download_products, name='download_products'),
    path('uploadsvg/', views.upload_svg, name='upload_svg'),
    path('filesfolders/', views.files_folders, name='files_folders'),
    path('deletefile/<int:id>', views.delete_file, name='delete_file'),
    path('deletefolder/<int:id>', views.delete_folder, name='delete_folder'),
    
]
