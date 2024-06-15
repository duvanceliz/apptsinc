from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import HttpResponse
from .models import Project, Product, Tabs, Dasboard, PanelItems, Items,Labels, Category, Subcategory
from .forms import CreateProject, CreateProduct, UploadProducts, CreateTab, SearchForm, CreatePage, UploadSVGForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import pandas as pd
import openpyxl
from django.http import JsonResponse
import json
from openpyxl.styles import Font, PatternFill
from .utils import print_data
import os
from django.conf import settings
from django.contrib import messages

# Create your views here.

@login_required
def home(request):
    projects = Project.objects.filter(usersesion=request.user)
    paginator = Paginator(projects, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user = request.user  # El usuario actualmente autenticado
    session_key = request.session.session_key 
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
                       
    return render(request, 'home.html',{'page_obj': page_obj, 'username':user.username, 'session_key':session_key, 'is_admin':is_admin})

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
        project = Project.objects.create(name = request.POST['name'], company_name = request.POST['company_name'], asesor = request.POST['asesor'], usersesion=request.user )
        return redirect('/')
    
@login_required
def product(request):
    product = Product.objects.all()
    paginator = Paginator(product, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product.html',{'page_obj': page_obj})


@login_required
def dashboard(request, id):
    dashboard = Dasboard.objects.get(id=id)
    tab = dashboard.tab
    panelitems = PanelItems.objects.all()
    categorys = Category.objects.all()
    subcategorys = Subcategory.objects.all()
    items = Items.objects.all()
    labels = Labels.objects.all()
    return render(request, 'dashboard.html',{'tab':tab, 'panelitems':panelitems, 'items': items, 'dashboard':dashboard, 'labels':labels, 'categorys':categorys, 'subcategorys':subcategorys, 'form':SearchForm()})

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
    
@login_required   
def upload_products(request):
    if request.method == 'POST':
        form = UploadProducts(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file, engine='openpyxl')

            products = Product.objects.all()
            products.delete()

            # print(df.iterrows())
            for _,row in df.iterrows():
                if pd.notna(row['Nombre del Producto / Servicio (obligatorio)']) and pd.notna( row['Referencia de Fábrica']) and pd.notna(row['Modelo'] ) and pd.notna(row['Marca'] ):
                    code = row['Código del Producto (obligatorio)'] if pd.notna(row['Código del Producto (obligatorio)']) else 'nn'
                    product_name = row['Nombre del Producto / Servicio (obligatorio)'] 
                    factory_ref = row['Referencia de Fábrica'] 
                    model = row['Modelo'] 
                    brand = row['Marca'] 
                    location = row['UBICACIÓN'] if pd.notna(row['UBICACIÓN']) else 'nn'
                    quantity = row['CANTIDAD'] if pd.notna(row['CANTIDAD']) else 0
                    description = row['ORBSERVACION'] if pd.notna(row['ORBSERVACION']) else 'nn'
        
                    product = Product.objects.create(
                        code=code,
                        product_name=product_name,
                        factory_ref=factory_ref,
                        model=model,
                        brand=brand,
                        location=location,
                        quantity= quantity,
                        description=description,
                    )
                    if product.description != 'nn':
                        description_list = product.description.split(",")
                    
                        PanelItems.objects.create(
                            img=description_list[0],
                            tag = description_list[1],
                            width = description_list[2],
                            product = product

                        )

            messages.success(request, 'Productos subidos y creados exitosamente.')
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
        print(request.POST)
        project = Project.objects.get(id=id)
        Tabs.objects.create(tab_name = request.POST['tab_name'], controller= request.POST['controller'], project= project)
        return redirect("/project/tabs/{}/".format(id))



@login_required
def delete_tab(request, id):
    object = get_object_or_404(Tabs, id=id)
    project = object.project
    object.delete()
    return redirect(f"/project/tabs/{project.id}/")

@login_required
def download_offer(request,id):
    project =Project.objects.get(id=id)
    tabs = project.tabs.all()
    equipos = Dasboard.objects.filter(tab__in=tabs).select_related('tab')
    items = Items.objects.filter(dashboard__in=equipos).select_related('dashboard')          
            # sheet.cell(row=i+3, column=9, value=controller.point)           
    def create_sheet(tabs):
        sheets = []
        for tab in tabs:
            sheet = workbook.create_sheet(title=tab.tab_name)
            sheets.append(sheet)
        return sheets
    
    workbook = openpyxl.Workbook()
    # sheet = workbook.active
    # sheet.title = 'TAB01'
    sheet_to_delete = workbook.active
    workbook.remove(sheet_to_delete)
    
    # header_font = Font(bold=True, color="FFFFFF")
    # header_fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
  
    units_list_tab =[]

    for tab in tabs:
        units =[]
        for equipo in equipos:
            if tab.id == equipo.tab.id:
                units.append(equipo)
        units_list_tab.append(units)

    sheets = create_sheet(tabs)

    for i in range(1,len(units_list_tab)+1):
        print_data(units_list_tab[i-1],items,sheets[i-1],project)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=C-1-552 CLEAN AIR.pdf'

    workbook.save(response)
    
    return response

    
@login_required
def save_items(request):

    if request.method == 'GET':
        return redirect('/')
    else:
        raw_data = request.body
        print(f"desde save_item: {raw_data}"  )
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
                item_exist.width = float(value['width'].replace("px",""))          
                item_exist.save()
            else:
                dashboard = get_object_or_404(Dasboard, id=int(data['dashboard_id'])) 
                new_item = Items(id_code=value['id_code'],
                                 x=value['x'],y=value['y'],
                                 width =float(value['width'].replace("px","")),
                                 relationship=value['relationship'], 
                                 img=img_obj, dashboard= dashboard)
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
                label_exist.save()
            else:
                dashboard = get_object_or_404(Dasboard, id=int(data['dashboard_id']))                         
                new_label = Labels(id_code=label['id_code'],value=label['value'],x=label['x'],y=label['y'],width =float(label['width'].replace("px","")),height=float(label['height'].replace("px","")), dashboard= dashboard )
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
    dashboard_products = []
    total_points_list = []
    items = Items.objects.all()
    dashboard = Dasboard.objects.get(id=request.GET['id'])
    for item in items:
        if dashboard.id == item.dashboard.id:
            if item.img.product != None:
                dashboard_products.append(item.img.product)
    total_set = set(dashboard_products)
    total = list(total_set)
    total_products = []
    points = ['BI','BO','AI','AO']
    subtotal = 0
    for p in total:
        count = 0
        for product in dashboard_products:
            if p.id == product.id:
                count += 1
        total_product = {}
        total_product['product']  = p
        total_product['quantity'] = count
        total_product['total_price'] = p.sale_price * count
        subtotal += p.sale_price * count
        total_products.append(total_product)
    for point in points:
        total = 0
        for total_product in total_products:
            if total_product['product'].point == point:
                total += total_product['quantity']
        total_points={}
        total_points['pointtype'] = point
        total_points['quantity'] = total
        total_points_list.append(total_points)
    print(total_points_list)

    return render(request, 'total.html', {'dashboard':dashboard,'items':items, 'total_products':total_products, 'subtotal':subtotal, 'total_points_list':total_points_list})



def handle_uploaded_file(file, path):
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def upload_svg(request):
    if request.method == 'POST' and request.FILES.getlist('files'):
        folder_name = request.POST.get('folder_name')
        tag = request.POST.get('tag')
        areproducts = request.POST.get('areproducts')
        
        files = request.FILES.getlist('files')
        if areproducts == 'on':
            for file in files:
                product = get_object_or_404(Product,model=file.name.split(".")[0])
                panelitem = PanelItems(img=f'img/{folder_name}/{file.name}', tag=tag, product=product )
                panelitem.save()
        else:
            for file in files:
                panelitem = PanelItems(img=f'img/{folder_name}/{file.name}', tag=tag )
                panelitem.save()

        
        # print(os.path.join(settings.BASE_DIR, 'tsinc','static', 'img', folder_name))        
        for file in files:
            # Define la ruta donde quieres guardar los archivos
            upload_dir = os.path.join(settings.BASE_DIR, 'tsinc','static', 'img', folder_name)
            os.makedirs(upload_dir, exist_ok=True)  # Crea la carpeta si no existe
            file_path = os.path.join(upload_dir, file.name)
            handle_uploaded_file(file, file_path)
            
        return HttpResponse('Archivos subidos exitosamente')
    
    return render(request, 'uploadsvg.html')

    




