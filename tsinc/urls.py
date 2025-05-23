from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ProductAutocomplete

urlpatterns = [
    path('', views.home, name='home' ),
    path('product-autocomplete/', ProductAutocomplete.as_view(), name='product-autocomplete'),
    path('project/create', views.create_project, name='create_project'),
    path('product/create', views.create_product, name='create_product'),
    path('project/delete/<int:id>/', views.delete_project, name='delete_obj'),
    path('show_inventory/', views.show_inventory, name='product' ),
    path('dashboard/<int:id>/', views.dashboard, name='dashboard' ),
    path('uploadproducts/', views.upload_products, name='uploadproducts' ),
    path('project/tabs/<int:id>/', views.tabs, name='tabs'),
    path('tab/delete/<int:id>/', views.delete_tab, name='delete_tab'),
    path('page/delete/<int:id>/', views.delete_page, name='delete_page'),
    path('downloadpoints/<int:id>/', views.download_points, name='download_points'),
    path('saveitems/', views.save_items, name='save_items'),
    path('page/create/<int:id>/', views.create_page, name='create_page'),
    path('deleteitem/', views.delete_item, name='delete_item'),
    path('productsearch/', views.product_search, name='product_search'),
    path('totalproducts/', views.total, name='total'),
    path('downloadproducts/', views.download_products, name='download_products'),
    path('uploadsvg/', views.upload_svg, name='upload_svg'),
    path('filesfolders/', views.files_folders, name='files_folders'),
    path('file/delete/<int:id>', views.delete_file, name='delete_file'),
    path('file_item/delete/<int:id>', views.delete_file_item, name='delete_file_item'),
    path('folder/delete/<int:id>', views.delete_folder, name='delete_folder'),
    path('edittab/<int:id>', views.edit_tab, name='edit_tab'),
    path('modifypoints/<int:id>', views.modify_points_file, name='modify_points'),
    path('controller/delete/<int:id>', views.delete_controller, name='delete_controller'),
    path('downloadpointexcel/<int:id>', views.download_point_excel, name='download_point_excel'),
    path('modifysuper/<int:id>', views.modify_supervisor, name='modify_super'),
    path('license/delete/<int:id>', views.delete_license, name='delete_license'),
    path('downloadoffer/<int:id>', views.download_offer, name='download_offer'),
    path('editpage/', views.edit_page, name='edit_page'),
    path('editproject/<int:id>', views.edit_project, name='edit_project'),
    path('product/delete/<int:id>', views.delete_product, name='delete_product'),
    path('editproduct/<int:id>', views.edit_product, name='edit_product'),
    path('remission/create', views.create_remission, name='create_remission'),
    path('remission/create/<int:project_id>', views.create_remission, name='create_remission'),
    path('addproducttobox/<int:id>', views.add_product_to_box, name='add_product_to_box'),
    path('addproduc/<int:id>', views.add_product, name='add_product'),
    path('subtractproduc/<int:id>', views.subtract_product, name='subtract_product'),
    path('cleanproductbox/', views.clean_productbox, name='clean_productbox'),
    path('remissions/', views.remissions, name='remissions'),
    path('remission/delete/<int:id>', views.delete_remission, name='delete_remission'),
    path('show_remission/<int:id>', views.show_remission, name='show_remission'),
    path('productshipped/', views.product_shipped, name='product_shipped'),
    path('order/create', views.create_order, name='create_order'),
    path('order/create/<int:project_id>', views.create_order, name='create_order'),
    path('savecar/', views.save_car, name='save_car'),
    path('purcharseorder/', views.purcharse_order, name='purcharse_order'),
    path('purcharseorderproducts/', views.purcharse_order_products, name='purcharse_order_products'),
    path('orderproductinfo/<int:id>', views.order_product_info, name='order_product_info'),
    path('downloadremission/<int:id>', views.download_remission, name='download_remission'),
    path('editremission/<int:id>', views.edit_remission, name='edit_remission'),
    path('editorder/<int:id>', views.edit_order, name='edit_order'),
    path('orderentry/create/<int:id>', views.create_order_entry, name='create_order_entry'),
    path('order/delete/<int:id>', views.delete_order, name='delete_order'),
    path('order_product/delete/<int:id>', views.delete_order_product, name='delete_order_product'),
    path('order_entry/delete/<int:id>', views.delete_order_entry, name='delete_order_entry'),
    path('downloadorder/<int:id>', views.download_order, name='download_order'),
    path('entryinfo/<int:id>', views.entry_info, name='entry_info'),
    path('statictics/orders', views.order_statictics, name='order_statictics'),
    path('productinfo/<int:id>', views.product_info, name='product_info'),
    path('addentryinventory/<int:id>', views.add_entry_inventory, name='add_entry_inventory'),
    path('remissionproduct/delete/<int:id>', views.delete_remission_product, name='delete_remission_product'),
    path('statictics/products', views.product_statictics, name='product_statictics'),
    path('statictics/remission', views.remission_statictics, name='remission_statictics'),
    path('addcarremission/<int:id>', views.add_car_remission, name='add_car_remission'),
    path('addcarorder/<int:id>', views.add_car_order, name='add_car_order'),
    path('duplicateremission/<int:id>', views.duplicate_remission, name='duplicate_remission'),
    path('duplicateorder/<int:id>', views.duplicate_order, name='duplicate_order'),
    path('accessdenied/', views.access_denied, name='access_denied'),
    path('carpage/', views.carpage, name='carpage'),
    path('savetrm/', views.save_trm, name='save_trm'),
    path('uploadremissionfile/<int:id>', views.upload_remission_file, name='upload_remission_file'),
    path('file/delete/<int:id>', views.delete_file, name='delete_file'),
    path('uploadorderfile/<int:id>', views.upload_order_file, name='upload_order_file'),
    path('orderfile/delete/<int:id>', views.delete_order_file, name='delete_order_file'),
    path('viewfile/<int:id>', views.view_file, name='view_file'),
    path('uploadproductfile/<int:id>', views.upload_product_file, name='upload_product_file'),
    path('productfile/delete/<int:id>', views.delete_product_file, name='delete_product_file'),
    path('invoice/create/<int:id>', views.create_invoice, name='create_invoice'),
    path('invoices/', views.invoices, name='invoices'),
    path('orderinvoice/create/<int:id>', views.create_order_invoice, name='create_order_invoice'),
    path('orderinvoice/delete/<int:id>', views.delete_order_invoice, name='delete_order_invoice'),
    path('show_all_offers/<int:approved>', views.show_all_offers, name='show_all_offers'),
    path('change_offer_status/<int:id>', views.change_offer_status, name='change_offer_status'),
    path('change_offer_status/<int:id>', views.change_offer_status, name='change_offer_status'),
    path('overview/', views.overview, name='overview'),
    path('new_folder/', views.new_folder, name='new_folder'),
    path('overview_folder/<int:id>', views.overview_folder, name='overview_folder'),
    path('update_folder/<int:id>', views.update_folder, name='update_folder'),
    path('update_tree_order/', views.update_tree_order, name='update_tree_order'),
    path('show_invoice/<int:id>', views.show_invoice, name='show_invoice'),
    path('invoice/delete/<int:id>', views.delete_invoice, name='delete_invoice'),
    path('update_invoice/<int:id>', views.update_invoice, name='update_invoice'),
    path('upload_invoice_file/<int:id>', views.upload_invoice_file, name='upload_invoice_file'),
    path('invoice_file/delete/<int:id>', views.delete_invoice_file, name='delete_invoice_file'),
    path('duplicate_invoice/<int:id>', views.duplicate_invoice, name='duplicate_invoice'),
    path('upload_folder_file/<int:id>', views.upload_folder_file, name='upload_folder_file'),
    path('upload_order_invoice_file/<int:id>', views.upload_order_invoice_file, name='upload_order_invoice_file'),
    path('docs/', views.docs, name='docs'),
    path('folder_item/delete/<int:id>', views.delete_folder_item, name='delete_folder_item'),
    path('edit_offer/<int:id>', views.edit_offer, name='edit_offer'),
    path('offer_item/delete/<int:id>', views.delete_offer_item, name='delete_offer_item'),
    path('save_offer_item/', views.save_offer_item, name='save_offer_item'),
    path('save_offer_item/', views.save_offer_item, name='save_offer_item'),
    path('add_from_car_to_offer/<int:section>/<int:tab_id>/<int:project_id>', views.add_from_car_to_offer, name='add_from_car_to_offer'),
    path('generate_offer/<int:id>', views.generate_offer, name='generate_offer'),
    # path('add_from_car_to_offer/<int:section>', views.add_from_car_to_offer, name='add_from_car_to_offer'),
    path('add_from_car_to_offer/<int:project_id>/<int:parent_id>', views.add_from_car_to_offer, name='add_from_car_to_offer'),
    path('change_to_purcharse_order/', views.change_to_purcharse_order, name='change_to_purcharse_order'),
    path('order_from_offer/create/<int:project_id>', views.create_order_from_offer, name='create_order_from_offer'),
    path('remission_from_offer/create/<int:project_id>', views.create_remission_from_offer, name='create_remission_from_offer'),
    path('add_car_to_invoice/<int:id>', views.add_car_to_invoice, name='add_car_to_invoice'),
    path('product_in_invoice/delete/<int:id>', views.delete_product_in_invoice, name='delete_product_in_invoice'),
    path('invoice_from_offercreate/<int:project_id>', views.create_invoice_from_offer, name='create_invoice_from_offer'),
    path('show_all_purcharse_order_invoices/', views.show_all_purcharse_order_invoices, name='show_all_purcharse_order_invoices'),
    path('download_categories/', views.download_categories, name='download_categories'),
    path('upload_categories/', views.upload_categories, name='upload_categories'),
    path('task/create/<int:project_id>', views.create_task, name='create_task'),
    path('custom_offer/', views.custom_offer, name='custom_offer'),
    path('productos/', views.obtener_productos, name='obtener_productos'),
    path('add_section/<int:project_id>', views.add_section, name='add_section'),
    path('offer_item/delete/<int:id>', views.delete_offer_item, name='delete_offer_item'),
    path('add_subtitle/<int:project_id>/<int:parent_id>', views.add_subtitle, name='add_subtitle'),
    path('show_all_activity/', views.show_all_activity, name='show_all_activity'),
    path('user_view/', views.user_view, name='user_view'),
    path('tasks/<int:project_id>', views.tasks, name='tasks'),
    path('save_order_container_task/', views.save_order_container_task, name='save_order_container_task'),
    path('comment/save/', views.save_comment, name='save_comment'),
    path('task/dalete/<int:id>', views.delete_task, name='delete_task'),
    path('task/edit/<int:id>', views.edit_task, name='edit_task'),
    path('upload_task_file/', views.upload_task_file, name='upload_task_file'),
    path('comment/dalete/<int:id>', views.delete_comment, name='delete_comment'),
    path('task/archive/<int:id>/<int:opt>', views.archive_task, name='archive_task'),
    path('archived_task_project/', views.archived_task_project, name='archived_task_project'),
    path('project/archive/<int:id>', views.archive_project, name='archive_project'),
    path('project/unarchive/<int:id>', views.unarchive_project, name='unarchive_project'),


] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




