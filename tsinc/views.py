from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import HttpResponse
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import pandas as pd
import openpyxl
from django.http import JsonResponse
import json
from .utils import print_data, print_calc_supervirsor, sort_list_point, modify_point_file, print_offer, print_notes
import os, shutil
from django.conf import settings
from django.contrib import messages
from django.db.models import Q

# Create your views here.

@login_required
def home(request):
    projects = Project.objects.filter(usersesion=request.user)
    tabs = Tabs.objects.filter(project__in=projects)
    pages = Dasboard.objects.filter(tab__in=tabs)
    paginator = Paginator(projects, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user = request.user  # El usuario actualmente autenticado
    session_key = request.session.session_key 
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
                       
    return render(request, 'home.html',{'page_obj': page_obj, 'username':user.username, 'session_key':session_key, 'is_admin':is_admin, 'tabs':tabs, 'pages':pages})

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
    
@login_required
def product(request):
    search = request.GET.get('search')
    print(search)
    if search:
        page_obj = Product.objects.filter(Q(product_name__icontains= search) | Q(model__icontains= search))
    else:
        search = "control"
        page_obj = Product.objects.filter(product_name__icontains= search)

    # product = Product.objects.all()
    # paginator = Paginator(product, 10)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    return render(request, 'product.html',{'page_obj': page_obj})


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

        project = Product.objects.create(code = request.POST['code'], product_name = request.POST['product_name'], factory_ref= request.POST['ref'], model= request.POST['model'], sale_price= request.POST['price'],iva=iva)
        return redirect('/product')


def verify_code_point_des(description):
    code = "NA"
    point = "NA"
    descrip = "NA"
    
    if pd.notna(description):
        description_list = description.split(",")
        code = description_list[0]
        point = description_list[1]
        descrip =  description_list[2]
    
    return code,point,descrip
        
    



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
                        
                        
                        product_exist = Product.objects.filter(model = model, brand = brand).exists()
                         
                        code,point,descrip = verify_code_point_des(description)
                            
                        if product_exist:
                            product= Product.objects.filter(model=model, brand=brand).first()
                            product.product_name = product_name
                            product.factory_ref = factory_ref
                            product.model = model
                            product.brand = brand
                            product.location = location
                            product.quantity = quantity
                            product.sale_price = sale_price
                            product.code = code
                            product.point = point
                            product.description = descrip
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
                            code = code,
                            point = point,
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
                    brand = row['brand']
                    location = row['location'] if pd.notna(row['location']) else 'NA'
                    quantity = row['quantity']
                    point = row['point'] if pd.notna(row['point']) else 'NA'
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
                        product.description = description
                        product.point = point
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

@login_required
def upload_svg(request):

    if request.method == 'POST' and request.FILES.getlist('files'):
        folder_name = request.POST.get('folder_name')
        tag = request.POST.get('tag')
        files = request.FILES.getlist('files')

        def validation_panelitem(file):
            panelitem_exists = PanelItems.objects.filter(name=file.name).exists()
            return panelitem_exists
            
       
        def validation_folder(folder_name):
            exist = Folders.objects.filter(name= folder_name).exists()
            return exist
            
            
        panelitem_exist = list(map(validation_panelitem, files))

    
        if not any(panelitem_exist):
            
            exist = validation_folder(folder_name)

            if not exist:
                folder = Folders.objects.create(
                        name= folder_name,
                        path = f'img/{folder_name}'
                    )
            else:

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

@login_required
def files_folders(request):
     
    panelitems = PanelItems.objects.all()
    folders = Folders.objects.all()
    
    return render(request, 'filesfolders.html', {
        'folders':folders,
        'panelitems': panelitems
    } )
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

@login_required
def edit_product(request):
    id = int(request.GET.get('id'))
    product = get_object_or_404(Product,id=id)
    if request.method == 'POST':
        code = request.POST.get('code')
        product_name = request.POST.get('product_name')
        factory_ref = request.POST.get('factory_ref')
        model = request.POST.get('model')
        sale_price = request.POST.get('sale_price')
        brand = request.POST.get('brand')
        location = request.POST.get('location')
        quantity = request.POST.get('quantity')
        point = request.POST.get('point')
        description = request.POST.get('description')
        product.code = code
        product.product_name = product_name
        product.factory_ref = factory_ref
        product.model = model
        product.sale_price = sale_price
        product.brand = brand
        product.location = location
        product.quantity = quantity
        product.point = point
        product.description = description
        product.save()
        messages.success(request,f"Cambios realizados correctamente")
        return redirect(f'/editproduct/?id={product.id}')
    
    return render(request,'editproduct.html',{'product':product})

