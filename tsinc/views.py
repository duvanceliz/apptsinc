from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Max
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
import pandas as pd
import openpyxl
from django.http import JsonResponse
import json
from .utils import print_data, print_calc_supervirsor, sort_list_point, modify_point_file, print_offer, print_notes, print_remission, print_order
import os, shutil
from django.conf import settings
from django.contrib import messages
from django.db.models import Q, F
import math
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField, F

# Create your views here.


def staff_required(user):
    return user.is_staff

def superuser_required(user):
    return user.is_superuser

def paginator(request, obj, number):
    paginator = Paginator(obj, number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


@login_required
def home(request):
    projects = Project.objects.filter(usersesion=request.user)
    tabs = Tabs.objects.filter(project__in=projects)
    pages = Dasboard.objects.filter(tab__in=tabs)

    page_obj = paginator(request,projects,5)
    user = request.user  # El usuario actualmente autenticado
    session_key = request.session.session_key 
    is_staff = staff_required(user) # Verifica si el usuario es administrador
                       
    return render(request, 'home.html',{'page_obj': page_obj, 'username':user.username, 'session_key':session_key, 'is_staff':is_staff, 'tabs':tabs, 'pages':pages})

@login_required
def delete_project(request, id):
    object = get_object_or_404(Project, id=id)
    object.delete()
    return redirect('/')

@login_required
def create_project(request):
    if request.method == 'GET':
       return render(request, 'createproject.html',{'form': CreateProject()})
    else:
        print(request.POST)
        project = Project.objects.create(name = request.POST['name'], company_name = request.POST['company_name'],nit=request.POST['nit'], asesor = request.POST['asesor'], usersesion=request.user )
        return redirect('/')

def replace_cero(value):
    if value == 0:
        value = 1
    return value

def seve_stat_prod(products):
    # products = Product.objects.all()
    
    for product in products:
        
        orderproduct = OrderProduct.objects.filter(product=product).all()
        total_entrys = OrderEntry.objects.filter(product__in= orderproduct).count()
        total_shippeds = ProductSent.objects.filter(product = product).count() 
             
        if total_entrys < total_shippeds:
            rotations = total_entrys
        elif total_shippeds < total_entrys:
            rotations = total_shippeds
        else:
            rotations = total_shippeds

        if product.quantity > product.min_stock:

            out_stock = 1

        else:

            out_stock = 0

        rotations = rotations

        # print(f"producto:{product.model}--Rotaciones:{rotations}--Fuera stock:{out_stock}")
        prod_stat_exist = ProductStatictics.objects.filter(product = product).exists()
        if prod_stat_exist:
            prod_stat = ProductStatictics.objects.filter(product = product).first()
            prod_stat.rotations = rotations
            prod_stat.out_stock = out_stock
            prod_stat.save()
        else:   
            ProductStatictics.objects.create(product=product, rotations = rotations, out_stock = out_stock)
   


@user_passes_test(staff_required,login_url='/accessdenied/')
@login_required
def product(request):

    search = request.GET.get('search')
    currency = Trm.objects.filter(currency = "usd").first()
    
    if search:
        page_obj = Product.objects.filter(Q(product_name__icontains= search) | Q(model__icontains= search))
    else:
        page_obj = Product.objects.all()
        # page_obj = Product.objects.filter(product_name__icontains= search)

    product_files = ProductFile.objects.all()
    products = Product.objects.all()

    product_files_info = [
    {'product_id': product.id, 
     'quantity': sum(1 for file in product_files if file.product.id == product.id)
    } 
    for product in products
    ]   

    is_staff = staff_required(request.user)

    page_obj = paginator(request,page_obj,20)
    return render(request, 'product.html',{'page_obj': page_obj,
                                           'is_staff':is_staff,
                                           'currency':currency,
                                           'product_files_info':product_files_info
                                           })


@login_required
def dashboard(request, id):
    dashboard = Dasboard.objects.get(id=id)
    tab = dashboard.tab
    project = tab.project
    tabs = project.tabs.all()
    pages = Dasboard.objects.filter(tab__in=tabs).select_related('tab')
    panelitems = PanelItems.objects.all()
    categorys = Category.objects.all()
    subcategorys = Subcategory.objects.all()
    items = Items.objects.all()
    labels = Labels.objects.all()
    return render(request, 'dashboard.html',{'tab':tab, 'panelitems':panelitems, 'items': items, 'dashboard':dashboard, 'labels':labels, 'categorys':categorys, 'subcategorys':subcategorys, 'pages':pages, 'form':SearchForm()})

@login_required
def product_search(request):
    if request.method == 'POST':
        raw_data = request.body
        body_unicode = raw_data.decode('utf-8')
        data = json.loads(body_unicode)
        results = Product.objects.filter(product_name__icontains= data['search']).values()
        results = list(results)
        return JsonResponse(results,safe=False)

@user_passes_test(staff_required,login_url='/accessdenied/')   
@login_required
def create_product(request):
    if request.method == 'GET':
       return render(request, 'createproduct.html',{'form': CreateProduct()})
    else:
        print(request.POST)
        if request.POST['iva'] == 'on':
            iva = True
        else:
            iva = False

        project = Product.objects.create(code = request.POST['code'], 
                                         product_name = request.POST['product_name'], 
                                         factory_ref= request.POST['ref'],
                                         brand= request.POST['brand'], 
                                         model= request.POST['model'], 
                                         location= request.POST['location'],
                                         quantity= request.POST['quantity'],
                                         purcharse_price= request.POST['purcharse_price'],
                                         sale_price= request.POST['sale_price'],
                                         min_stock= request.POST['min_stock'],
                                         point= request.POST['point'],
                                         observation= request.POST['observation'],
                                         description= request.POST['description'],
                                         iva=iva)
        return redirect('/product')


def verify_code_point_des(description):
    code = "NA"
    point = "NA"
    descrip = "NA"
    min_stock = 0
    
    if pd.notna(description):
        description_list = description.split(",")
        if len(description_list) == 4:
            code = description_list[0]
            min_stock = description_list[1]
            point = description_list[2]
            descrip =  description_list[3]
    
    return code,min_stock,point,descrip
        
@user_passes_test(staff_required,login_url='/accessdenied/')    
@login_required   
def upload_products(request):
    if request.method == 'POST':
        form = UploadProducts(request.POST, request.FILES)
    
        if form.is_valid():
            excel_file = request.FILES['file']
            try:
                original = request.POST['original']
            except:
                original = None

            df = pd.read_excel(excel_file, engine='openpyxl')

            if not original:

                for _,row in df.iterrows():
                    if  pd.notna(row['Nombre del Producto / Servicio (obligatorio)']) and pd.notna( row['Referencia de Fábrica']) and pd.notna(row['Modelo'] ) and pd.notna(row['Marca'] ):
                        product_name = row['Nombre del Producto / Servicio (obligatorio)'] 
                        factory_ref = row['Referencia de Fábrica'] 
                        model = row['Modelo'] 
                        brand = row['Marca'] 
                        location = row['UBICACIÓN'] if pd.notna(row['UBICACIÓN']) else 'NA'
                        quantity = row['CANTIDAD'] if pd.notna(row['CANTIDAD']) else 0
                        description = row['ORBSERVACION']
                        sale_price = row['Precio de venta 12'] if pd.notna(row['Precio de venta 12']) else 0
                        purcharse_price = row['Precio de venta 11'] if pd.notna(row['Precio de venta 11']) else 0
                        
                        product_exist = Product.objects.filter(model = model, brand = brand).exists()
                         
                        code,min_stock,point,descrip = verify_code_point_des(description)
                            
                        if product_exist:
                            product= Product.objects.filter(model=model, brand=brand).first()
                            product.product_name = product_name
                            product.factory_ref = factory_ref
                            product.model = model
                            product.brand = brand
                            product.location = location
                            product.quantity = quantity
                            product.sale_price = sale_price
                            product.purcharse_price = purcharse_price
                            product.code = code
                            product.point = point
                            product.description = descrip
                            product.min_stock = min_stock
                            product.save()
                        
                        else:
                                                        
                            product = Product.objects.create(
                            product_name=product_name,
                            factory_ref=factory_ref,
                            model=model,
                            brand=brand,
                            location=location,
                            quantity= quantity,
                            sale_price = sale_price,
                            purcharse_price = purcharse_price,
                            code = code,
                            point = point,
                            min_stock = min_stock,
                            description=descrip,
                            )
                messages.success(request, 'Productos subidos y creados exitosamente.')
            else:
                for _,row in df.iterrows():
                    code = row['code'] if pd.notna(row['code']) else 'NA'
                    product_name = row['product_name']
                    factory_ref = row['factory_ref']
                    model = row['model']
                    sale_price = row['sale_price']
                    purcharse_price = row['purcharse_price']
                    brand = row['brand']
                    location = row['location'] if pd.notna(row['location']) else 'NA'
                    quantity = row['quantity']
                    min_stock = row['min_stock']
                    point = row['point'] if pd.notna(row['point']) else 'NA'
                    observation = row['observation'] if pd.notna(row['observation']) else 'NA'
                    description = row['description'] if pd.notna(row['description']) else 'NA'
                    iva = row['iva']

                    product_exist = Product.objects.filter(model = model, brand = brand ).exists()

                    if product_exist:
                        product= Product.objects.get(model=model, brand=brand)
                        product.code = code
                        product.product_name = product_name
                        product.factory_ref = factory_ref
                        product.model = model
                        product.brand = brand
                        product.location = location
                        product.quantity = quantity
                        product.sale_price = sale_price
                        product.purcharse_price = purcharse_price
                        product.point = point
                        product.min_stock = min_stock
                        product.observation = observation
                        product.description = description
                        product.iva = iva
                        product.save()
                    else:
                         product = Product.objects.create(
                                code = code,
                                product_name = product_name,
                                factory_ref = factory_ref,
                                model = model,
                                brand = brand,
                                location = location,
                                quantity = quantity,
                                sale_price = sale_price,
                                purcharse_price = purcharse_price,
                                min_stock = min_stock,
                                description = description,
                                point = point,
                                iva = iva,
                         )


                messages.success(request, 'Productos subidos y creados exitosamente.')

                
            # messages.error(request, 'No se pudieron subir los productos a la base de datos, porfavor verifica que tu tabla tenga todos los parametros esten llenos')

            
            return redirect('/uploadproducts')
    else:
        form = UploadProducts()
    return render(request, 'uploadproducts.html', {'form': form})

@login_required
def download_products(request):
    # Consulta todos los datos del modelo
    queryset = Product.objects.all().values()
    # Convierte el queryset a un DataFrame de pandas
    df = pd.DataFrame(queryset)

    # Crear una respuesta HTTP con el tipo de contenido de Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=tabla.xlsx'

    # Guardar el DataFrame en el archivo Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')
    return response


@login_required
def tabs(request, id):
    if request.method == 'GET':
        project = Project.objects.get(id=id)
        tabs = project.tabs.all()
        # tabs = offer.tabs.all()
        return render(request,'tabs.html',{'tabs': tabs, 'form': CreateTab(), 'project':project})
    else:
        
        project = Project.objects.get(id=id)
        chest_type = True
        if request.POST['chest_type'] == "2":
            chest_type = False 
        Tabs.objects.create(tab_name = request.POST['tab_name'], chest_type = chest_type, controller= request.POST['controller'], project= project)
        return redirect("/project/tabs/{}/".format(id))

@login_required
def delete_tab(request, id):
    object = get_object_or_404(Tabs, id=id)
    project = object.project
    object.delete()
    return redirect(f"/project/tabs/{project.id}/")

@login_required
def download_points(request,id):
    project =Project.objects.get(id=id)
    tabs = project.tabs.all()
    pages = Dasboard.objects.filter(tab__in=tabs).select_related('tab')
    items = Items.objects.filter(dashboard__in=pages).select_related('dashboard') 
    labels = Labels.objects.filter(dashboard__in=pages).select_related('dashboard')  

    
    parent_labels = [ label for label in labels if label.relationship != 'None'] 
        
    data = [ {
            'tab_name': label.dashboard.tab.tab_name,
            'unit_name': label.value,
            'related_items': [ item for item in items if label.relationship == item.relationship and item.img.product != None]
        }
        for label in parent_labels
        ]
    
    # print(pd.DataFrame(data))
    
    
    # sheet.cell(row=i+3, column=9, value=controller.point) 

    def create_sheet(tabs):
        sheets = [ workbook.create_sheet(title=tab.tab_name) for tab in tabs if tab.chest_type]
        return sheets
    try:
        workbook = openpyxl.Workbook()
        # # sheet = workbook.active
        # # sheet.title = 'TAB01'

        sheet_to_delete = workbook.active
        workbook.remove(sheet_to_delete)
    
   
    
        sheets = create_sheet(tabs)
        
        
        sheet = Sheet.objects.filter(project = project).all()
        
        sheet.delete()
    
        c_quantity = 0

   

        for i in range(0,len(tabs)):
            if tabs[i].chest_type:
                c_quantity += 1
                print_data(data,tabs[i],sheets[i],project)

        
        try: 
            sv_tab = [tab for tab in tabs if not tab.chest_type][0]
        except:
            sv_tab = None
        
        if sv_tab:
            sheet_supervisor = workbook.create_sheet(title='Supervisor')
            print_calc_supervirsor(sheet_supervisor,sv_tab,c_quantity,project)
        
        path = os.path.join(settings.BASE_DIR, 'tsinc','static', 'points','Points.xlsx')
        workbook.save(path)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=Points.xlsx'

        workbook.save(response)
        return response
    except:
        messages.error(request,"¡Ha ocurrido un error al momento de generar el archivo!, asegurese de haber creado tableros, paginas y equipos en la dashboard. si el problema persiste contacte a la empresa.")
        return redirect('/')
    

    
@login_required
def save_items(request):

    if request.method == 'GET':
        return redirect('/')
    else:
        raw_data = request.body
        # print(f"desde save_item: {raw_data}"  )
        body_unicode = raw_data.decode('utf-8')
        data = json.loads(body_unicode)
        for value in data['values']:
            img_obj = PanelItems.objects.get(id=value['pk'])
            try:
                item_exist = Items.objects.get(id_code = value['id_code'])
            except ObjectDoesNotExist:
                item_exist = None
            
            if item_exist:
                item_exist.x = value['x']
                item_exist.y = value['y']
                item_exist.zindex = int(value['zindex'])
                item_exist.relationship=value['relationship']
                item_exist.tag = value['tag']
                # item_exist.width = float(value['width'].replace("px",""))          
                item_exist.save()
            else:
                dashboard = get_object_or_404(Dasboard, id=int(data['dashboard_id'])) 
                new_item = Items(id_code=value['id_code'],
                                 x=value['x'],y=value['y'],
                                #  width =float(value['width'].replace("px","")),
                                 relationship=value['relationship'], 
                                 img=img_obj, tag=value['tag'], dashboard= dashboard)
                new_item.save()

        for label in data['labels']:
            try:
                label_exist = Labels.objects.get(id_code = label['id_code'])
            except ObjectDoesNotExist:
                label_exist = None

            if label_exist:
                label_exist.value = label['value']
                label_exist.x = label['x']
                label_exist.y = label['y']
                label_exist.zindex = int(label['zindex'])
                label_exist.width = float(label['width'].replace("px",""))
                label_exist.height = float(label['height'].replace("px",""))
                label_exist.relationship=label['relationship']
                label_exist.save()
            else:
                dashboard = get_object_or_404(Dasboard, id=int(data['dashboard_id']))                         
                new_label = Labels(id_code=label['id_code'],
                                   value=label['value'],
                                   x=label['x'],y=label['y'],
                                   width =float(label['width'].replace("px","")),
                                   height=float(label['height'].replace("px","")), 
                                   relationship=label['relationship'],
                                   dashboard= dashboard )
                new_label.save()
       
        return JsonResponse({'mensaje': 'Datos guardados con éxito!'})
    
@login_required
def create_page(request,id):
    if request.method == 'GET':
        tab = get_object_or_404(Tabs,id=id)
        pages_tab = tab.dashboards.all()
        # page = Dasboard.objects.all()
        paginator = Paginator(pages_tab, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'createpage.html',{'page_obj': page_obj, 'form':CreatePage(), 'tab':tab})
    else:
        tab = Tabs.objects.get(id=id)
        Dasboard.objects.create(name = request.POST['name'], tab=tab)
        return redirect(f'/createpage/{id}/')

@login_required
def delete_page(request, id):
    object = get_object_or_404(Dasboard, id=id)
    tab = object.tab
    object.delete()
    return redirect(f'/createpage/{tab.id}/')
@login_required
def delete_item(request):
    if request.method == 'POST':
        raw_data = request.body
        # print(f"desde delete_item: {raw_data}")
        body_unicode = raw_data.decode('utf-8')
        data = json.loads(body_unicode)
        for item in data['id_code']:
            try: 
                item_exist = Items.objects.get(id_code = item)     
            except ObjectDoesNotExist:
                item_exist = None
            if item_exist:
                item_exist.delete()
            else:
                labels = get_object_or_404(Labels,id_code=item)
                labels.delete()
        return JsonResponse({'mensaje': 'eliminado con éxito!'})
    

@login_required
def total(request):
    total_points_list = []
    dashboard = Dasboard.objects.get(id=request.GET['id'])
    items = Items.objects.filter(dashboard = dashboard).all()
   
    dashboard_products = [ item.img.product for item in items if item.img.product != None]

    total = list(set(dashboard_products))
 
    total_products = []

    points = ['BI','BO','AI','AO']

    subtotal = 0
    
    def clean_point(point):
        point_cleaned = ""
        for i in point:
            if not i.isnumeric():
                point_cleaned += i
        return point_cleaned

    for p in total:
        count = 0
        for product in dashboard_products:
            if p.id == product.id:
                count += 1
        total_product = {}
        total_product['product']  = p
        total_product['pointtype'] = clean_point(p.point)
        total_product['quantity'] = count
        total_product['total_price'] = p.sale_price * count
        subtotal += p.sale_price * count
        total_products.append(total_product)
    
    for point in points:
        total = 0
        for product in total_products:
            if product['pointtype'] == point:
                total += product['quantity']
        total_points={}
        total_points['pointtype'] = point
        total_points['quantity'] = total
        total_points_list.append(total_points)

    return render(request, 'total.html', {'dashboard':dashboard,'items':items, 'total_products':total_products, 'subtotal':subtotal, 'total_points_list':total_points_list})



def handle_uploaded_file(file, path):
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


@user_passes_test(staff_required,login_url='/accessdenied/')
@login_required
def upload_svg(request):

    if request.method == 'POST' and request.FILES.getlist('files'):#verifica si el metodo es post y si exiten archivos
        folder_name = request.POST.get('folder_name') #nombre de la carpeta
        tag = request.POST.get('tag') #etiqueta 
        files = request.FILES.getlist('files') #archivos

        def validation_panelitem(file):#valida que exita el item de panel
            panelitem_exists = PanelItems.objects.filter(name=file.name).exists()
            return panelitem_exists
            
       
        def validation_folder(folder_name):#valida que exista el folter
            exist = Folders.objects.filter(name= folder_name).exists()
            return exist
            
            
        panelitem_exist = list(map(validation_panelitem, files)) #con la funcion map valida cada uno de los archivos y devuelve una lista de booleanos

    
        if not any(panelitem_exist):
            
            exist = validation_folder(folder_name)

            if not exist:# si no existe el folder entra y lo crea
                folder = Folders.objects.create(
                        name= folder_name,
                        path = f'img/{folder_name}'
                    )
            else:# De lo contrario lo busca en la base de datos

                folder = Folders.objects.get(name=folder_name)
                 
            def save_panelitem(file):
                
                # product = get_object_or_404(Product,model=file.name.split(".")[0])
                product_exist = Product.objects.filter(model=file.name.split(".")[0]).exists()

                if product_exist:
                    product = Product.objects.get(model=file.name.split(".")[0])
                    panelitem = PanelItems(name=file.name,  
                                        img=f'img/{folder_name}/{file.name}', 
                                        tag=tag, product=product, folder= folder)
                    panelitem.save()
                else:
                    panelitem = PanelItems(name=file.name,  
                                        img=f'img/{folder_name}/{file.name}', 
                                        tag=tag,folder= folder)
                    panelitem.save()
                    
                return panelitem
                    
            saved_panelitem = list(map(save_panelitem,files))

            panelitem_names = [ item.name for item in saved_panelitem]
            
            def filter_no_porduct(panelitem):
                if not panelitem.product:
                    return panelitem

            panelitem_no_product = list(filter(filter_no_porduct,saved_panelitem))
            panelitem_no_product_str = [ panelitem.name for panelitem in panelitem_no_product]
                
        # print(os.path.join(settings.BASE_DIR, 'tsinc','static', 'img', folder_name))        
            for file in files:
                # Define la ruta donde quieres guardar los archivos
                upload_dir = os.path.join(settings.BASE_DIR, 'tsinc','static', 'img', folder_name)
                os.makedirs(upload_dir, exist_ok=True)  # Crea la carpeta si no existe
                file_path = os.path.join(upload_dir, file.name)
                handle_uploaded_file(file, file_path)
           
           
           
            messages.success(request, f"{', '.join(panelitem_names)} Elementos subidos exitosamente.")

        

            if len(panelitem_no_product) != 0:
                messages.info(request, f"{', '.join(panelitem_no_product_str)} Elementos no han sido relacionado con ningun producto.")
        else:

            panelitems = [ file.name for file in files if PanelItems.objects.filter(name= file.name).exists()]

            messages.error(request, f"Los elementos: {', '.join(panelitems)} ya existen en la base de datos") 
          
              
               
        return redirect('/uploadsvg')

    folders = Folders.objects.all()
    return render(request, 'uploadsvg.html', {'folders':folders})

@user_passes_test(staff_required,login_url='/accessdenied/')
@login_required
def files_folders(request):
     
    panelitems = PanelItems.objects.all()
    folders = Folders.objects.all()
    
    return render(request, 'filesfolders.html', {
        'folders':folders,
        'panelitems': panelitems
    } )

@user_passes_test(staff_required,login_url='/accessdenied/')
@login_required
def delete_file(request, id):

    try:
        panelitem = PanelItems.objects.get(id=id)
    except ObjectDoesNotExist:
        panelitem = None
    
    file_path = os.path.join(settings.BASE_DIR, 'tsinc','static', os.path.normpath(panelitem.img) )

  
    if panelitem and os.path.exists(file_path):
        panelitem.delete()
        os.remove(file_path)
        messages.success(request,f"El acrchivo {panelitem.name} ha sido eliminado correctamente")
    else:
        messages.error(request,'El archivo no se encontró!!')
        
    

    return redirect('/filesfolders')

@user_passes_test(staff_required,login_url='/accessdenied/')
@login_required
def delete_folder(request, id):
    
    try:
        folder = Folders.objects.get(id=id)
    except ObjectDoesNotExist:
        folder = None
    
    folder_path = os.path.join(settings.BASE_DIR, 'tsinc','static', os.path.normpath(folder.path) )

  
    if folder and os.path.exists(folder_path):
        folder.delete()
        shutil.rmtree(folder_path)
        messages.success(request,f"La carpeta {folder.name} ha sido eliminada correctamente")
    else:
        messages.error(request,'La carpeta no se encontró!!')
        
    return redirect('/filesfolders')
@login_required
def edit_tab(request):
    id = int(request.GET.get('id'))
    tab = get_object_or_404(Tabs,id=id)
    if request.method == 'POST':
        tab_name = request.POST.get('tab')
        option = request.POST.get('option')
        if option == '1':
            controller = "LG BECON CONTROLLER"
        elif option == '2':
            controller = "JCI FACILITY EXPLORER"
        elif option == '3':
            controller = "JCI METASYS"
        tab.tab_name = tab_name
        tab.controller = controller
        tab.project = tab.project
        tab.save()
        messages.success(request,f"El tablero {tab.tab_name} ha sido guardado correctamente.")
        return redirect(f'/edittab/?id={tab.id}')
    
    return render(request,'edittab.html',{'tab':tab})

@login_required
def modify_points_file(request,id):
    try:
        if request.method == "GET":
            project = Project.objects.get(id=id)
            sheets = project.sheet.all()
            sheet_id = request.GET.get("sheet")
            licenses = License.objects.filter(sheet__in =sheets)
            sv = False
            if sheet_id:
                sheet = Sheet.objects.filter(id=sheet_id).first()
                points = Points.objects.filter(sheet = sheet).all()
                if sheet.name == "Supervisor":
                    sv=True 
            else:
                sheet = sheets[0]
                points = Points.objects.filter(sheet = sheet).all()
            
            return render(request,"modifypoint.html",{'sheets':sheets, 
                                                    'points':points, 
                                                    'addcontroller':AddController(), 
                                                    'addlicense':AddLicense(), 
                                                    'sheet_id':sheet.id,
                                                    'project':project,
                                                    'licenses':licenses,
                                                    'sv':sv
                                                    }
                                                    
                                                    )
        else:
            def is_controller(string):
                for l in string:
                    if l == "C":
                        return True 
                return False
                
            sheet = Sheet.objects.filter(id=request.POST.get("sheet_id")).first()
            try:
                request_license = request.POST["license"]
            except:
                request_license = None
            if not request_license:
                controller = Product.objects.filter(id=request.POST["controller"]).first()
                
                if not  controller.point == None:
                    points = controller.point.split("-")
                    sort_points = sort_list_point(points)

                    Points.objects.create(name = controller.model,
                                        is_controller = is_controller(controller.code),
                                        eu=sort_points[0],
                                        ed=sort_points[1],
                                        sa=sort_points[2],
                                        sd=sort_points[3],
                                        sc=sort_points[4],
                                        sheet = sheet
                                        )
                else:
                    Points.objects.create(name = controller.model,
                                        is_controller = is_controller(controller.code),
                                        sheet = sheet
                                        )

            else:
                # print(request.POST["license"])
                license = Product.objects.filter(id=request.POST["license"]).first()
                License.objects.create(name=license.model,description=license.description, sheet=sheet)

            return redirect(f"/modifypoints/{id}?sheet={sheet.id}")
    except:
        messages.error(request,"¡Ha ocurrido un error para generar la información!, asegurese de haber descargado el archivo de puntos previamente. si el problema persiste contacte a la empresa.")
        return redirect('/')


def delete_controller(request, id):
    controller = Points.objects.filter(id=id).first()
    sheet = controller.sheet
    print(sheet.project)
    controller.delete()
    return redirect(f"/modifypoints/{sheet.project.id}?sheet={sheet.id}")

def download_point_excel(request,id):
    project = Project.objects.get(id=id)
    path = os.path.join(settings.BASE_DIR, 'tsinc','static', 'points','Points.xlsx')
    workbook = openpyxl.load_workbook(path)
    
    for sheet_name in workbook.sheetnames:
        modify_point_file(project,workbook[sheet_name])
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Points.xlsx'

    workbook.save(response)
    
    return response

def modify_supervisor(request, id):
    return render(request,"modifysuper.html")

def delete_license(request, id):
    license = License.objects.filter(id=id).first()
    sheet = license.sheet
    license.delete()
    return redirect(f"/modifypoints/{sheet.project.id}?sheet={sheet.id}")

@login_required
def download_offer(request,id):

    try:
        project =Project.objects.get(id=id)
        workbook = openpyxl.Workbook()
        # # sheet = workbook.active
        # # sheet.title = 'TAB01'

        sheet_to_delete = workbook.active
        workbook.remove(sheet_to_delete)

        sheet = workbook.create_sheet(title="Oferta")
        sheet_notes = workbook.create_sheet(title="NOTAS Y ACLARACIONES")

        print_offer(sheet,project)
        print_notes(sheet_notes,project)
        # path = os.path.join(settings.BASE_DIR, 'tsinc','static', 'points','Points.xlsx')
        # workbook.save(path)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=Oferta.xlsx'

        workbook.save(response)

        return response
    except:
        messages.error(request,"¡Ha ocurrido un error al momento de generar el archivo!, asegurese de haber creado tableros, paginas y equipos en la dashboard. si el problema persiste contacte a la empresa.")
        return redirect('/')



@login_required
def edit_page(request):
    id = int(request.GET.get('id'))
    page = get_object_or_404(Dasboard,id=id)
    if request.method == 'POST':
        page_name = request.POST.get('page_name')
        page.name = page_name
        page.save()
        messages.success(request,f"Cambios realizados correctamente a {page.name}")
        return redirect(f'/editpage/?id={page.id}')
    
    return render(request,'editpage.html',{'page':page})

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def edit_project(request):
    id = int(request.GET.get('id'))
    project = get_object_or_404(Project,id=id)
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        company_name = request.POST.get('company_name')
        nit = request.POST.get('nit')
        project.name = project_name
        project.company_name = company_name
        project.nit = nit
        project.save()
        messages.success(request,f"Cambios realizados correctamente")
        return redirect(f'/editproject/?id={project.id}')
    
    return render(request,'editproject.html',{'project':project})


@login_required
def delete_product(request, id):
    product = Product.objects.filter(id=id).first()
    product.delete()
    return redirect(f"/product/")

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def edit_product(request,id):
    product = Product.objects.filter(id = id).first()
    if request.method == 'POST':
        product = Product.objects.filter(id = id).first()
        code = request.POST.get('code')
        product_name = request.POST.get('product_name')
        factory_ref = request.POST.get('factory_ref')
        model = request.POST.get('model')
        sale_price = request.POST.get('sale_price')
        purcharse_price = request.POST.get('purcharse_price')
        brand = request.POST.get('brand')
        location = request.POST.get('location')
        quantity = request.POST.get('quantity')
        point = request.POST.get('point')
        observation = request.POST.get('observation')
        description = request.POST.get('description')
        min_stock = request.POST.get('min_stock')
        product.code = code
        product.product_name = product_name
        product.factory_ref = factory_ref
        product.model = model
        product.sale_price = sale_price
        product.purcharse_price = purcharse_price
        product.brand = brand
        product.location = location
        product.quantity = quantity
        product.point = point
        product.observation = observation
        product.description = description
        product.min_stock = min_stock
        product.save()
        messages.success(request,f"Cambios realizados correctamente")
        return redirect(f'/editproduct/{product.id}')
    
    is_staff = staff_required(request.user)
    return render(request,'editproduct.html',{'product':product, 'is_staff':is_staff})
    


@login_required
def add_product_to_box(request,id): 
    product = Product.objects.filter(id=id).first()
    user = request.user
    if ProductBox.objects.filter(product = product, usersession = request.user).exists():
        productbox = ProductBox.objects.filter(product = product).first()
        productbox.quantity +=1
        productbox.save() 
        messages.success(request,f"El producto {product.model} ya se encontraba en el carrito ahora tienes {productbox.quantity}.")
    else:
        ProductBox.objects.create(product = product, quantity = 1, price =product.sale_price, usersession = user) 
        messages.success(request,f"El producto {product.model} ha sido agregado al carrito.")
    return redirect('/product/')

@login_required
def add_product(request,id):
    if request.method == "POST":
        print(request.POST.get(f"quantity{id}"))
    # print(request.GET.get(f"quantity{id}"))
    # productbox = ProductBox.objects.filter(id = id).first()
    # productbox.quantity +=1
    # productbox.save() 
        # messages.success(request,f"El producto {product.model} ya se encontraba en el carrito ahora tienes {productbox.quantity}.")
    return redirect('/createremission/')

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def subtract_product(request,id,path): 

    productbox = ProductBox.objects.filter(id = id).first()
    productbox.delete()
        # messages.success(request,f"El producto {product.model} ya se encontraba en el carrito ahora tienes {productbox.quantity}.")
    return redirect(f"/{path}/")


def increase_code():
    remission_code = OfferCode.objects.filter(name = "remission").first()

    new_code = int(remission_code.code) + 1

    remission_code.code = new_code

    remission_code.save()

    return remission_code

@user_passes_test(staff_required,login_url='/accessdenied/')
@login_required
def create_remission(request): 
    if request.method == 'GET':
        path = "createremission"

        productbox = ProductBox.objects.filter(usersession = request.user).all()
        is_staff = staff_required(request.user)
        return render(request,'createremission.html',{'productbox':productbox,
                                                      'form':CreateRemission,'path':path,'is_staff':is_staff})
    else:
        productbox = ProductBox.objects.filter(usersession = request.user).all()

        
        for productb in productbox:
            if productb.quantity > productb.product.quantity:
                messages.error(request,f"No hay sufiente cantidad del producto {productb.product.model} en el inventario")
                return redirect("/createremission/")

        remission_code = increase_code()

        remission = Remission.objects.create(city = request.POST['city'],
                                            number = remission_code.code,
                                            order_number = request.POST['order_number'],
                                            company = request.POST['company'],
                                            nit = request.POST['nit'],
                                            location = request.POST['location'],
                                            project = request.POST['project'],
                                            responsible = request.POST['responsible'],
                                            observation = request.POST['observation'],
                                            usersession = request.user
                                            )
        products = []
        for productb in productbox:
            productsent = ProductSent.objects.create(
                product = productb.product,
                quantity = productb.quantity,
                price = productb.price,
                remission = remission
            )
            product = Product.objects.filter(id= productsent.product.id).first()
            products.append(product)
            product.quantity -= productsent.quantity
            product.save()
        
        seve_stat_prod(products)

        messages.success(request,f"La remisión ha sido generada correctamente.")

        return redirect("/createremission/")
    
@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def clean_productbox(request,path):  
    productbox = ProductBox.objects.all()
    productbox.delete()
    return redirect(f"/{path}/")

@user_passes_test(staff_required,login_url='/accessdenied/')
@login_required
def remissions(request):  
    remissions = Remission.objects.filter().order_by('-date').all()
    search = request.GET.get('search')
    if search:
        remissions = Remission.objects.filter(Q(company__icontains= search) | Q(project__icontains= search) | Q(number__icontains= search))
    
    remission_files = RemissionFile.objects.all()
    
    remission_files_info = [
    {'remission_id': remission.id, 
     'quantity': sum(1 for file in remission_files if file.remission.id == remission.id)
    } 
    for remission in remissions
    ]         

    remissions = paginator(request,remissions,10)

    is_staff = staff_required(request.user)

    return render(request,'remissions.html',{'remissions':remissions, 
                                             'is_staff':is_staff,
                                             'remission_files_info':remission_files_info
                                             })

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def delete_remission(request,id):  
    remission = Remission.objects.filter(id = id).first()
    remission_prod = ProductSent.objects.filter(remission = remission ).all()
    for prod in remission_prod:
        product = Product.objects.filter(id = prod.product.id).first()
        product.quantity += prod.quantity
        product.save()
    remission.delete()
    return redirect("/remissions/")


@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def product_remission(request,id):  
    remission = Remission.objects.filter(id=id).first()
    products = ProductSent.objects.filter(remission= remission).all()
    remissionfiles = RemissionFile.objects.filter(remission = remission).all()
    is_staff = staff_required(request.user)
    return render(request,'productremission.html',{'products':products, 
                                                   'remission':remission, 
                                                   'remissionfiles':remissionfiles,'is_staff':is_staff})

@user_passes_test(staff_required,login_url='/accessdenied/')
@login_required
def product_shipped(request):  
    products_shipped = ProductSent.objects.all()[:10]
    search = request.GET.get('search')
    if search:
        products = Product.objects.filter(Q(product_name__icontains= search) | Q(model__icontains= search))
        products_shipped = ProductSent.objects.filter(product__in = products)
    is_staff = staff_required(request.user)   
    return render(request,'productshipped.html',{'products':products_shipped,'is_staff':is_staff})

def calc_t_quantity_price(order):
    
    orderproducts = OrderProduct.objects.filter(order = order).all()
    t_quantity = 0
    t_price = 0

    for product in orderproducts:
        t_quantity += product.quantity 
        t_price += product.price * product.quantity

    order.total_quantity = t_quantity
    order.total_price = t_price

    order.save()

def calc_progress(order):

    order_entrys = OrderEntry.objects.filter(order = order).all()
    arrived = 0
   
    for entry in order_entrys:
        arrived += entry.quantity
    
    if order.total_quantity > 0:
        progress = math.ceil((arrived * 100) / order.total_quantity)
    else:
        progress = 0

    order.progress = progress
    order.save()

def increase_code_order():

    code = OfferCode.objects.filter(name = "order").first()

    code_splited = code.code.split("-")

    new_code = int(code_splited[-1]) + 1

    code.code = f"{code_splited[0]}-{new_code}"

    code.save()

    return code

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def create_order(request): 
    if request.method == 'GET':
        path = "createorder"
        productbox = ProductBox.objects.filter(usersession = request.user).all()
        is_staff = staff_required(request.user)
        return render(request,"createorder.html",{'productbox':productbox,
                                                  'form':CreateOrder(),
                                                   'path':path,
                                                   'is_staff':is_staff
                                                     })

    else:
        productbox = ProductBox.objects.filter(usersession = request.user).all()
        tracking = request.POST['tracking']
        supplier = request.POST['supplier']
        nit = request.POST['nit']
        address = request.POST['address']
        phone = request.POST['phone']
        customer = request.POST['customer']
        cost_center = request.POST['cost_center']
        inspector = request.POST['inspector']
        supervisor = request.POST['supervisor']
        observation = request.POST['observation']
        currency = request.POST['currency']
    
        code = increase_code_order()

        order = PurcharseOrder.objects.create(code = code.code,
                                              tracking = tracking,
                                              supplier = supplier,
                                              nit = nit,
                                              address = address,
                                              phone = phone,
                                              customer = customer,
                                              cost_center = cost_center,
                                              inspector = inspector,
                                              supervisor = supervisor,
                                              observation = observation,
                                              currency = currency,
                                              usersession = request.user
                                             )
        for product in productbox:

            OrderProduct.objects.create(
                product = product.product,
                quantity = product.quantity,
                price = product.price,
                order = order
            )
        
        calc_t_quantity_price(order)

        messages.success(request,f"La orden de compra ha sido generada correctamente.")
            
        return redirect("/createorder/")
    
@login_required
def save_car(request):
    if request.method == "POST":
        raw_data = request.body
        # print(f"desde save_item: {raw_data}"  )
        body_unicode = raw_data.decode('utf-8')
        data = json.loads(body_unicode)
        for product in data['values']:
            productbox = ProductBox.objects.filter(id= product['id']).first()
            productbox.quantity = product['quantity']
            productbox.price = product['price']
            productbox.save()
        return JsonResponse({'mensaje': 'Datos guardados con éxito!'})

@user_passes_test(staff_required,login_url='/accessdenied/')
@login_required
def purcharse_order(request):  
    orders = PurcharseOrder.objects.filter().order_by('progress').all()
    search = request.GET.get('search')
    if search:
        orders = PurcharseOrder.objects.filter(Q(code__icontains= search) | Q(supplier__icontains= search) | Q(tracking__icontains= search))

    orders = paginator(request,orders,10)

    order_files = OrderFile.objects.all()

    order_files_info = [
    {'order_id': order.id, 
     'quantity': sum(1 for file in order_files if file.order.id == order.id)
    } 
    for order in orders
    ] 

    is_staff = staff_required(request.user)
    return render(request,'purcharseorders.html',{'orders':orders, 
                                                  'is_staff':is_staff,
                                                  'order_files_info':order_files_info
                                                  })

@user_passes_test(staff_required,login_url='/accessdenied/')
@login_required
def purcharse_order_products(request):  
    purcharse_order_products = OrderProduct.objects.all()[:10]
    search = request.GET.get('search')
    if search:
        products = Product.objects.filter(Q(product_name__icontains= search) | Q(model__icontains= search))
        purcharse_order_products = OrderProduct.objects.filter(product__in = products)  

    is_staff = staff_required(request.user)   
    return render(request,'purcharseorderproducts.html',{'products':purcharse_order_products,'is_staff':is_staff})


def calc_info_order_product(orderproducts,orderentry):
    info_per_product = []
    for product in orderproducts:
        t_quantity = 0
        t_price = 0
        p={}
        for entry in orderentry:
            if product.id == entry.product.id:
                t_quantity += entry.quantity

        p['id'] = product.id
        p['t_quantity'] = t_quantity
        p['leftover'] = product.quantity - t_quantity      
        info_per_product.append(p)
    return info_per_product

@user_passes_test(staff_required,login_url='/accessdenied/')   
@login_required
def order_product_info(request,id):  
    order = PurcharseOrder.objects.filter(id=id).first()
    products = OrderProduct.objects.filter(order= order).all()
    orderentry = OrderEntry.objects.filter(order = order).all()
    orderfiles = OrderFile.objects.filter(order = order).all()
    
    most_recent_entry = OrderEntry.objects.filter(order = order).order_by("-date").first()
    
    intial_date = order.date

    if most_recent_entry:
        final_date = most_recent_entry.date
        
        # intial_date = datetime.date(2023, 6, 1)
        # final_date = datetime.datetime(2023, 7, 25)
        difference = final_date - intial_date
        delivery_time = difference.days
    else:
        delivery_time = 0

    arrived = 0
    d_price = 0

    for entry in orderentry:
        arrived += entry.quantity 
        d_price += entry.product.price * entry.quantity
    
    
    
    total_info = {
        't_price':round(order.total_price,2),
        'd_price':round(d_price,2),
        'r_price':round(order.total_price - d_price,2),
        't_quantity':order.total_quantity,
        'arrived':arrived,
        'leftover':round(order.total_quantity - arrived,2)
    }

    badge = ""

    if order.currency:
        badge = "COP"
    else:
        badge = "USD"
    
    info_per_product = calc_info_order_product(products,orderentry)
    
    is_staff = staff_required(request.user)

    return render(request,'orderproductinfo.html',{'products':products, 
                                                   'order':order, 
                                                   'orderentry':orderentry,
                                                   'total_info':total_info,
                                                   'info_per_product':info_per_product,
                                                   'delivery_time':delivery_time,
                                                   'badge':badge,
                                                   'orderfiles':orderfiles,
                                                   'is_staff':is_staff
                                                   
                                                   })


@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def download_remission(request,id):

    try:
        remission =Remission.objects.get(id=id)
        workbook = openpyxl.Workbook()
        # # sheet = workbook.active
        # # sheet.title = 'TAB01'

        sheet_to_delete = workbook.active
        workbook.remove(sheet_to_delete)

        sheet = workbook.create_sheet(title="Remision")

        print_remission(sheet,remission)
        # path = os.path.join(settings.BASE_DIR, 'tsinc','static', 'points','Points.xlsx')
        # workbook.save(path)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f"attachment; filename=Remision_{remission.number}.xlsx"

        workbook.save(response)

        return response
    except TypeError as e:
        messages.error(request,f"¡Ha ocurrido un error al momento de generar el archivo!.{e}")
        return redirect('/remissions/')

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def download_order(request,id):

    try:
        order =PurcharseOrder.objects.get(id=id)
        workbook = openpyxl.Workbook()
        # # sheet = workbook.active
        # # sheet.title = 'TAB01'

        sheet_to_delete = workbook.active
        workbook.remove(sheet_to_delete)

        sheet = workbook.create_sheet(title="Orden de compra")

        print_order(sheet,order)
        # path = os.path.join(settings.BASE_DIR, 'tsinc','static', 'points','Points.xlsx')
        # workbook.save(path)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f"attachment; filename=Orden_de_compra_{order.code}.xlsx"

        workbook.save(response)

        return response
    except TypeError as e:
        messages.error(request,f"¡Ha ocurrido un error al momento de generar el archivo!.{e}")
        return redirect('/purcharseorder/')


@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def edit_remission(request,id):
    remission = get_object_or_404(Remission,id=id)
    products = ProductSent.objects.filter(remission = remission).all()
    if request.method == 'POST':
        city = request.POST.get('city')
        company = request.POST.get('company')
        nit = request.POST.get('nit')
        location = request.POST.get('location')
        project = request.POST.get('project')
        responsible = request.POST.get('responsible')
        observation = request.POST.get('observation')
        remission.city = city
        remission.company = company
        remission.nit = nit
        remission.location = location
        remission.project = project
        remission.responsible = responsible
        remission.observation = observation
        remission.save()
        messages.success(request,f"Cambios realizados correctamente")
        return redirect(f'/editremission/{id}')
    is_staff = staff_required(request.user)
    return render(request,'editremission.html',{'remission':remission, 'products':products, 'is_staff':is_staff})

@user_passes_test(staff_required,login_url='/accessdenied/')     
@login_required
def edit_order(request,id):
    order = get_object_or_404(PurcharseOrder,id=id)
    orderproducts = OrderProduct.objects.filter(order = order).all()
    if request.method == 'POST':
        code = request.POST.get('code')
        tracking = request.POST.get('tracking')
        supplier = request.POST.get('supplier')
        nit = request.POST.get('nit')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.POST.get('customer')
        cost_center = request.POST.get('cost_center')
        inspector = request.POST.get('inspector')
        supervisor = request.POST.get('supervisor')
        observation = request.POST.get('observation')
        currency = request.POST.get('currency')
        order.tracking = tracking
        order.code = code
        order.supplier = supplier
        order.nit = nit 
        order.address = address
        order.phone = phone
        order.customer = customer
        order.cost_center = cost_center
        order.inspector = inspector
        order.supervisor = supervisor
        order.observation = observation
        order.currency = currency
        order.save()
        messages.success(request,f"Cambios realizados correctamente")
        return redirect(f'/editorder/{id}')
    is_staff = staff_required(request.user)

    return render(request,'editorder.html',{'order':order,'orderproducts':orderproducts, 'is_staff':is_staff})

      
@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def create_order_entry(request,id):

    order = get_object_or_404(PurcharseOrder,id=id)
    orderproducts = OrderProduct.objects.filter(order = order).all()
    orderentry = OrderEntry.objects.filter(order=order).order_by("-date").all()

    info_per_product = calc_info_order_product(orderproducts,orderentry)

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        tracking = request.POST.get('tracking')
        if not product_id == 'None':
            orderproduct = OrderProduct.objects.filter(id=product_id).first()
            if orderproduct.order.trm != 0:
                price_dollar = round(orderproduct.price / orderproduct.order.trm,2)
                orderentry = OrderEntry.objects.create(order = order, 
                                      product = orderproduct, 
                                      quantity=quantity,
                                      price = price_dollar,
                                      tracking=tracking,
                                      )
            else:
                orderentry = OrderEntry.objects.create(order = order, 
                                      product = orderproduct, 
                                      quantity=quantity,
                                      price = orderproduct.price,
                                      tracking=tracking,
                                      )
            
            entries = OrderEntry.objects.filter(product__product__id = orderproduct.product.id).all()
            
            currency = Trm.objects.filter(currency = "usd").first()
            prices = []
            for entry in entries:
                if entry.order.currency:
                    if currency.value > 0:
                        price_usd = round(entry.price / currency.value,2)
                        prices.append(price_usd)
                else:
                    prices.append(entry.price)
            
            highest_price =  max(prices)
            product = Product.objects.filter(id = orderproduct.product.id).first()
            product.purcharse_price = highest_price
            product.quantity += int(orderentry.quantity)
            product.save()
            calc_progress(order)
            seve_stat_prod([product])
            messages.success(request,f"La entrada ha sido creada correctamente")

        else:

            messages.error(request,f"No puedes generar mas entradas, Todos los productos han sido entregados!")
        return redirect(f'/createorderentry/{id}')
    is_staff = staff_required(request.user)
    return render(request,'createorderentry.html',{'order':order,
                                                   'orderproducts':orderproducts, 
                                                   'orderentry':orderentry,
                                                   'info_per_product':info_per_product,
                                                   'is_staff':is_staff
                                                   })

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def delete_order(request,id):  
    order = PurcharseOrder.objects.filter(id = id).first()
    order.delete()
    return redirect("/purcharseorder/")


@login_required
def delete_order_product(request,id):  
    orderproduct = OrderProduct.objects.filter(id = id).first()
    order = PurcharseOrder.objects.filter(id = orderproduct.order.id).first()
    orderproducts = OrderProduct.objects.filter(order = order).all()
    orderproduct.delete()
    calc_t_quantity_price(order)
    calc_progress(order)
    return redirect(f"/editorder/{orderproduct.order.id}")

@login_required
def delete_order_product(request,id):  
    orderproduct = OrderProduct.objects.filter(id = id).first()
    order = PurcharseOrder.objects.filter(id = orderproduct.order.id).first()
    orderproduct.delete()
    calc_t_quantity_price(order)
    calc_progress(order)
    return redirect(f"/editorder/{order.id}")

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def delete_order_entry(request,id):  
    orderentry = OrderEntry.objects.filter(id = id).first()
    order = PurcharseOrder.objects.filter(id = orderentry.order.id).first()
    product = Product.objects.filter(id = orderentry.product.product.id).first()
    product.quantity -= orderentry.quantity
    product.save()
    orderentry.delete()
    calc_t_quantity_price(order)
    calc_progress(order)
    return redirect(f"/createorderentry/{order.id}")


@login_required
def entry_info(request,id): 
    entry = OrderEntry.objects.filter(id=id).first()
    return render(request,"entryinfo.html",{'entry':entry})



@user_passes_test(superuser_required,login_url='/accessdenied/')
@login_required
def order_statictics(request): 
    # data = {
    #     'labels': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo'],
    #     'values': [10, 20, 30, 40, 50]
    # }
    most_recent_entry = OrderEntry.objects.all().order_by("-date")[:5]
    most_recent_order = PurcharseOrder.objects.all().order_by("-date")[:5]
    purcharseorders = PurcharseOrder.objects.all()
    entrys = OrderEntry.objects.all()
    currency = Trm.objects.filter(currency="usd").first()

    total_price = 0
    total_delivered = 0


    for order in purcharseorders:
        if order.progress != 100:
            if order.currency:
                if currency.value > 0:
                    total_price += round(order.total_price / currency.value,2)
            else:
                total_price += order.total_price

            for entry in entrys:
                if order.id == entry.order.id:
                    if order.currency:
                        total_delivered += (entry.product.price/currency.value) * entry.quantity
                    else:
                        total_delivered += entry.product.price * entry.quantity
    
    total_delivered = round(total_delivered,2)
    # difference = final_date - intial_date
    # delivery_time = difference.days



    # pending_orders = [ order for order in purcharseorders if order.progress != 100]

    pending_orders = [{
        'order':order,
        'ago':order.date
    }
    for order in purcharseorders if order.progress != 100
    ][:5]

   
    total_info ={
        'total_orders': round(total_price,2),
        'total_delivered':round(total_delivered,2),
        'total_remaining': round(total_price - total_delivered,2)

    }
    return render(request,"orderstatictics.html",{
                                                  'recent_entrys':most_recent_entry,
                                                  'recent_orders':most_recent_order,
                                                  'total_info':total_info,
                                                  'pending_orders':pending_orders,
                                        
                                                    })

@login_required
def product_info(request,id): 
    product = Product.objects.filter(id=id).first()
    products = Product.objects.all()
    orderproduct = OrderProduct.objects.filter(product = product).all()
    orderentry = OrderEntry.objects.filter(product__in= orderproduct ).order_by("-date")[:5]
    products_shipped = ProductSent.objects.filter(product = product).order_by('-remission__date')[:5]
    total_entrys = OrderEntry.objects.filter(product__in= orderproduct).count()
    total_shippeds = ProductSent.objects.filter(product = product).count() 
    rotations = 0
    if total_entrys < total_shippeds:
        rotations = total_entrys
    elif total_shippeds < total_entrys:
        rotations = total_shippeds
    else:
        rotations = total_shippeds

    product_files = ProductFile.objects.filter(product = product).all()
 
    is_staff = staff_required(request.user)
    return render(request,"productinfo.html",{'product':product, 
                                              'orderentry':orderentry, 
                                              'products_shipped':products_shipped, 
                                              'total_entrys':total_entrys,
                                              'total_shippeds':total_shippeds,
                                              'rotations':rotations,
                                              'product_files':product_files,
                                              'is_staff':is_staff
                                              })

@login_required
def add_entry_inventory(request,id):
    entry = OrderEntry.objects.filter(id = id).first()
    product = Product.objects.filter(id = entry.product.product.id).first()
    if not entry.added:
        entry.added = True
        entry.save()
        product.quantity += entry.quantity
        product.save()
    return redirect(f"/createorderentry/{entry.order.id}")


@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def delete_remission_product(request,id):  
    remissionproduct = ProductSent.objects.filter(id = id).first()
    product = Product.objects.filter(id = remissionproduct.product.id).first()

    product.quantity += remissionproduct.quantity

    product.save()
    
    remissionproduct.delete()

    return redirect(f"/editremission/{remissionproduct.remission.id}")

@user_passes_test(superuser_required,login_url='/accessdenied/')
@login_required
def product_statictics(request):
    products = Product.objects.all()
    prod_out_stock = ProductStatictics.objects.order_by("out_stock")[:10]
    prod_rotations = ProductStatictics.objects.order_by("-rotations")[:10]
    expensive_prod = Product.objects.order_by("-sale_price")[:10]
    cheaper_prod = Product.objects.order_by("sale_price")[:10]

    seve_stat_prod(products)

    total_inventory = 0
    total_inventory_cop = 0

    for product in products:
        total_inventory += product.purcharse_price * product.quantity
        total_inventory_cop += product.purcharse_price_cop * product.quantity
    
    total_inventory = round(total_inventory,2)
    total_inventory_cop = round(total_inventory_cop,2)
    return render(request,"productstatictics.html",{'prod_out_stock':prod_out_stock,
                                                    'prod_rotations':prod_rotations,
                                                    'total_inventory':total_inventory,
                                                    'total_inventory_cop':total_inventory_cop,
                                                    'exp_prod':expensive_prod,
                                                    'cheaper_prod':cheaper_prod
                                                    
                                                    })

@user_passes_test(superuser_required,login_url='/accessdenied/')
@login_required
def remission_statictics(request):
    remissions = Remission.objects.order_by('-date')[:10]
    prod_remission = ProductSent.objects.order_by('-remission__date')[:10]

    return render(request,"remissionstatictics.html",{'remissions':remissions,'prod':prod_remission})


@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def add_car_remission(request,id):
    productbox = ProductBox.objects.filter(usersession = request.user).all()
    remission = Remission.objects.filter(id = id).first()

    for productb in productbox:
            if productb.quantity > productb.product.quantity:
                messages.error(request,f"No hay sufiente cantidad del producto {productb.product.model} en el inventario")
                return redirect(f"/editremission/{remission.id}")
    products = []
    for productb in productbox:
        productsent = ProductSent.objects.create(
            product = productb.product,
            quantity = productb.quantity,
            price = productb.price,
            remission = remission
        )
        product = Product.objects.filter(id= productsent.product.id).first()
        products.append(product)
        product.quantity -= productsent.quantity
        product.save()
    
    seve_stat_prod(products)

    return redirect(f"/editremission/{remission.id}")
    

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def add_car_order(request,id):
    productbox = ProductBox.objects.filter(usersession = request.user).all()
    order = PurcharseOrder.objects.filter(id = id).first()


    for product in productbox:

            OrderProduct.objects.create(
                product = product.product,
                quantity = product.quantity,
                price = product.price,
                order = order
            )
        
    calc_t_quantity_price(order)
    calc_progress(order)

    return redirect(f"/editorder/{order.id}")

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def duplicate_remission(request,id):
    remission = Remission.objects.filter(id = id).first()
    
    try:
        remission_code = increase_code()

        Remission.objects.create(
            number = remission_code.code,
            city = remission.city,
            company = remission.company,
            nit = remission.nit,
            location = remission.location,
            project = remission.project,
            responsible = remission.responsible,
            observation = remission.observation,
            order_number = remission.order_number,
            usersession = request.user
        )
        messages.success(request,"La remisión se ha duplicado con éxito")
    except TypeError as e:
         messages.error(request,f"Se ha presentado el siguiente error: {e}")
    return redirect("/remissions/")

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required 
def duplicate_order(request,id):
    order = PurcharseOrder.objects.filter(id = id).first()
    
    try:
        code = increase_code_order()

        PurcharseOrder.objects.create(
                                    code = code.code,
                                    tracking = order.tracking,
                                    supplier = order.supplier,
                                    nit = order.nit,
                                    address = order.address,
                                    phone = order.phone,
                                    customer = order.customer,
                                    cost_center = order.cost_center,
                                    inspector = order.inspector,
                                    supervisor = order.supervisor,
                                    observation = order.observation,
                                    usersession = request.user  
                                        )
        messages.success(request,"La orden de compra se ha duplicado con éxito")
       
    except TypeError as e:
         
        messages.error(request,f"Se ha presentado el siguiente error: {e}")

    return redirect("/purcharseorder/")

def access_denied(request):
    return render(request,"accessdenied.html")

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def carpage(request):
    productbox = ProductBox.objects.filter(usersession = request.user).all()
    path = "carpage"
    return render(request,"carpage.html",{'productbox':productbox,'path':path})

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def save_trm(request):

    if request.method == "POST":
        if Trm.objects.filter(currency = "usd").exists():
            currency = Trm.objects.filter(currency = "usd").first()
            currency.value = request.POST.get('trmvalue')
            currency.save()
        else:
            Trm.objects.create(currency="usd",value = request.POST.get('trmvalue'))
        
        products = Product.objects.all()
        currency = Trm.objects.filter(currency = "usd").first()
    
        for product in products:
            sale_price_cop = round(currency.value * product.sale_price,2)
            purcharse_price_cop = round(currency.value * product.purcharse_price,2)
            product.sale_price_cop = sale_price_cop
            product.purcharse_price_cop = purcharse_price_cop
            product.save()

    messages.success(request,f"Se ha establecido el TRM de: {currency.value} a todos los productos")    

    return redirect("/product/")


@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def upload_remission_file(request,id):
    remission = Remission.objects.filter(id = id).first()
    if request.method == "POST":
        form = UploadRemissionFile(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_without_space = file.name.replace(" ", "_")

            remission_file_exists = RemissionFile.objects.filter(name=file_without_space,remission = remission).exists()

            if remission_file_exists:
                remission_file = RemissionFile.objects.filter(name=file_without_space).first()

                upload_dir = os.path.join(settings.MEDIA_ROOT, "remission_files", f"{remission.number}")
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, file_without_space)
                handle_uploaded_file(file, file_path)

                messages.info(request,f"El archivo {remission_file.name} ya existe, ha sido reemplazado")
                return redirect(f"/uploadremissionfile/{remission.id}")
            
            else:
                remission_file = RemissionFile.objects.create(name = file_without_space,
                                                            remission=remission,
                                                            usersession = request.user
                                                            )  
            
            upload_dir = os.path.join(settings.MEDIA_ROOT, "remission_files", f"{remission.number}")
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, file_without_space)
            handle_uploaded_file(file, file_path)


            
            messages.success(request,f"El archivo {remission_file.name} ha sido cargado correctamente")

        return redirect(f"/uploadremissionfile/{remission.id}")
    
    is_staff = staff_required(request.user)
    
    return render(request,"uploadremissionfile.html",{'form':UploadRemissionFile, 'is_staff':is_staff, 'remission':remission})


@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def view_file(request,id,code):

    is_staff = staff_required(request.user)

    if code == "re":
        remission_file = get_object_or_404(RemissionFile,id=id)
        # Construir la URL del archivo
        file_url = os.path.join(settings.MEDIA_URL, "remission_files", f"{remission_file.remission.number}", remission_file.name)

        return render(request, "view_file.html", {"file_url": file_url, 
                                                  "file_name": remission_file.name,
                                                  "is_staff":is_staff
                                                  })
    elif code == "oc":
            
        order_file = get_object_or_404(OrderFile,id=id)
         # Construir la URL del archivo
        file_url = os.path.join(settings.MEDIA_URL, "order_files", f"{order_file.order.code}", order_file.name)

        return render(request, "view_file.html", {"file_url": file_url, 
                                                  "file_name": order_file.name,
                                                  "is_staff":is_staff
                                                  })
    elif code == "p":
            
        product_file = get_object_or_404(ProductFile,id=id)
         # Construir la URL del archivo
        file_url = os.path.join(settings.MEDIA_URL, "product_files", f"{product_file.product.id}", product_file.name)

        return render(request, "view_file.html", {"file_url": file_url, 
                                                  "file_name": product_file.name,
                                                  "is_staff":is_staff
                                                  })


@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def delete_remission_file(request,id):
    remission_file = get_object_or_404(RemissionFile,id=id)
    file_path = os.path.join(settings.MEDIA_ROOT, "remission_files", f"{remission_file.remission.number}", remission_file.name)
    
    if os.path.exists(file_path):
        os.remove(file_path) 
    
    remission_file.delete()

    return redirect(f"/productremission/{remission_file.remission.id}")

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def upload_order_file(request,id):
    order = PurcharseOrder.objects.filter(id = id).first()
    if request.method == "POST":
        form = UploadOrderFile(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_without_space = file.name.replace(" ", "_")
            order_file_exists = OrderFile.objects.filter(name=file_without_space,order = order).exists()

            if order_file_exists:
                order_file = OrderFile.objects.filter(name=file_without_space).first()

                upload_dir = os.path.join(settings.MEDIA_ROOT, "order_files", f"{order.code}")
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, file_without_space)
                handle_uploaded_file(file, file_path)

                messages.info(request,f"El archivo {order_file.name} ya existe, ha sido reemplazado")
                return redirect(f"/uploadorderfile/{order.id}")
            
            else:
                order_file = OrderFile.objects.create(name = file_without_space,
                                                            order=order,
                                                            usersession = request.user
                                                            )  
            
            upload_dir = os.path.join(settings.MEDIA_ROOT, "order_files", f"{order.code}")
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, file_without_space)
            handle_uploaded_file(file, file_path)


            messages.success(request,f"El archivo {order_file.name} ha sido cargado correctamente")

        return redirect(f"/uploadorderfile/{order.id}")
    
    is_staff = staff_required(request.user)
    
    return render(request,"uploadorderfile.html",{'form':UploadOrderFile, 
                                                      'is_staff':is_staff, 
                                                      'order':order})

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required   
def delete_order_file(request,id):
    order_file = get_object_or_404(OrderFile,id=id)
    file_path = os.path.join(settings.MEDIA_ROOT, "order_files", f"{order_file.order.code}", order_file.name)
    
    if os.path.exists(file_path):
        os.remove(file_path) 
    
    order_file.delete()

    return redirect(f"/orderproductinfo/{order_file.order.id}")


@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def upload_product_file(request,id):
    product = Product.objects.filter(id = id).first()
    if request.method == "POST":
        form = UploadProductFile(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_without_space = file.name.replace(" ", "_")
            product_file_exists = ProductFile.objects.filter(name=file_without_space,product = product).exists()

            if product_file_exists:

                product_file = ProductFile.objects.filter(name=file_without_space).first()
                upload_dir = os.path.join(settings.MEDIA_ROOT, "product_files", f"{product.id}")
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, file_without_space)
                handle_uploaded_file(file, file_path)
                messages.info(request,f"El archivo {product_file.name} ya existe, ha sido reemplazado")
                return redirect(f"/uploadproductfile/{product.id}")
            
            else:
                product_file = ProductFile.objects.create(name = file_without_space,
                                                            product=product,
                                                            usersession = request.user
                                                            )  
            
            upload_dir = os.path.join(settings.MEDIA_ROOT, "product_files", f"{product.id}")
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, file_without_space)
            handle_uploaded_file(file, file_path)


            messages.success(request,f"El archivo {product_file.name} ha sido cargado correctamente")

        return redirect(f"/uploadproductfile/{product.id}")
    
    is_staff = staff_required(request.user)
    
    return render(request,"uploadproductfile.html",{'form':UploadOrderFile, 
                                                      'is_staff':is_staff, 
                                                      'product':product})

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required    
def delete_product_file(request,id):
    product_file = get_object_or_404(ProductFile,id=id)
    file_path = os.path.join(settings.MEDIA_ROOT, "product_files", f"{product_file.product.id}", product_file.name)
    
    if os.path.exists(file_path):
        os.remove(file_path) 
    
    product_file.delete()

    return redirect(f"/productinfo/{product_file.product.id}")

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def create_invoice(request):
    if request.method == "POST":
        number = request.POST['number']
        total_price = request.POST['total_price']
        iva = request.POST['iva']
        source_retention = request.POST['source_retention']
        ica_retention = request.POST['ica_retention']
        Invoice.objects.create(
            number = number,
            total_price = total_price,
            iva = iva,
            source_retention = source_retention,
            ica_retention = ica_retention,
            usersession = request.user
        )
        messages.success(request,"La factura ha sido creado correctamente")
        return redirect(f"/createinvoice/")
    
    return render(request,"create_invoice.html",{'form':CreateInvoice})

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def invoices(request):
    
    invoices = Invoice.objects.filter().order_by('-date').all()
    search = request.GET.get('search')
    if search:
        invoices = Invoice.objects.filter(Q(number__icontains= search) | Q(total_price__icontains= search))
    
    
    invoices = paginator(request,invoices,10)

    return render(request,"invoices.html",{
        'invoices':invoices
    })

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def create_order_invoice(request,id):
    order = get_object_or_404(PurcharseOrder,id=id)
    

    if request.method == "POST":
        value_paid = request.POST.get('amount_to_pay')
        iva = request.POST.get('iva')
        source_retention = request.POST.get('source_retention')
        ica_retention = request.POST.get('ica_retention')
        OrderInvoice.objects.create(
            order = order,
            value_paid = value_paid,
            iva = iva,
            source_retention = source_retention,
            ica_retention = ica_retention,
            usersession = request.user
        )

    return render(request,"create_order_invoice.html",{
        'order':order
    })

@user_passes_test(staff_required,login_url='/accessdenied/') 
@login_required
def workspace(request):
    root_folders =  Folder.objects.filter(parent__isnull=True)

    def get_subfolders(folder):
        """Función recursiva para obtener las subcarpetas."""
        subfolders = folder.children.all()
        return [{'folder': sub, 'subfolders': get_subfolders(sub)} for sub in subfolders]
    
    # Construir la estructura de árbol
    folder_tree = [{'folder': folder, 'subfolders': get_subfolders(folder)} for folder in root_folders]

    is_staff = staff_required(request.user)
    
    context = {
        'folder_tree': folder_tree, 
        'is_staff':is_staff 
    }

    return render(request,"workspace.html",context)








