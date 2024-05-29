from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import Project, Product, Offers, TabUnits, Tabs, Slots, Dasboard, PanelItems, Items,Labels
from .forms import CreateProject, CreateProduct, UploadProducts, CreateOffer, CreateTab, CreateUnit, Units, SearchForm, CreatePage
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import pandas as pd
import openpyxl
from django.http import JsonResponse
import json
# Create your views here.

@login_required
def home(request):
    projects = Project.objects.all()
    paginator = Paginator(projects, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html',{'page_obj': page_obj})

def delete_project(request, id):
    object = get_object_or_404(Project, id=id)
    object.delete()
    return redirect('/')


def create_project(request):
    if request.method == 'GET':
       return render(request, 'createproject.html',{'form': CreateProject()})
    else:
        print(request.POST)
        project = Project.objects.create(name = request.POST['name'], dibujante = request.POST['dibujante'], approved = request.POST['approved'] )
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
    project = dashboard.project
    panelitems = PanelItems.objects.all()
    items = Items.objects.all()
    labels = Labels.objects.all()
    return render(request, 'dashboard.html',{'project':project, 'panelitems':panelitems, 'items': items, 'dashboard':dashboard, 'labels':labels })



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
    
def upload_products(request):
    if request.method == 'POST':
        form = UploadProducts(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file, engine='openpyxl')

            print(df.iterrows())
            for _,row in df.iterrows():
                
                Product.objects.create(
                    code=row['codigo'],
                    product_name=row['nombre'],
                    factory_ref=row['referencia'],
                    model=row['modelo'],
                    brand=row['marca'],
                    location=row['ubicacion'],
                    quantity=row['cantidad'],
                    sale_price=row['precio']
                )
            return redirect('/uploadproducts')
    else:
        form = UploadProducts()
    return render(request, 'uploadproducts.html', {'form': form})


def offer(request):
    if request.method == 'GET':
        offer = Offers.objects.all()
        paginator = Paginator(offer, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'offer.html',{'page_obj': page_obj, 'form':CreateOffer()})
    else:
        print(request.POST)
        Offers.objects.create(title = request.POST['title'], controller = request.POST['controller'])
        return redirect('/offer')


def tabs(request, id):
    if request.method == 'GET':
        offer = Offers.objects.get(id=id)
        tabs = offer.tabs.all()
        # tabs = offer.tabs.all()
        return render(request,'tabs.html',{'tabs': tabs, 'form': CreateTab() , 'offer': offer})
    else:
        print(request.POST)
        offer = Offers.objects.get(id=id)
        Tabs.objects.create(tab_name = request.POST['tab_name'],offer = offer)
        return redirect("/offer/tabs/{}/".format(id))



def units(request, id):
    if request.method == 'GET':
        tab = Tabs.objects.get(id=id)
        offer = tab.offer
        units = tab.units.all()
        # tabs = offer.tabs.all()
        return render(request,'units.html',{'units': units, 'form':CreateUnit(), 'offer': offer, 'tab': tab})
    else:
        print(request.POST)
        tab = Tabs.objects.get(id=id)
        unit_name = Units.objects.get(id=request.POST['unit'])
        TabUnits.objects.create(unit = unit_name , quantity = request.POST['quantity'], tab = tab)
        return redirect("/offer/tabs/units/{}/".format(id))


def config(request, id):
    if request.method == 'GET':

        search = request.GET.get('search')
        page_number = request.GET.get('page')          
        results = []
        unit = TabUnits.objects.get(id=id)
        slots = unit.slots.all()
        products = Product.objects.all()
        paginator = Paginator(products, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if search:
            results = Product.objects.filter(product_name__icontains=search)
            paginator = Paginator(results, 10)
            page_obj = paginator.get_page(page_number)
            
  

        return render(request, 'configuration.html',{'unit': unit, 'slots':slots, 'page_obj': page_obj, 'form':SearchForm()})
    else:
        unit = TabUnits.objects.get(id=id)
        prod = Product.objects.get(id=request.POST.get('productid'))
        Slots.objects.create(slot=prod, unit=unit)
        return redirect("/offer/tabs/units/configuration/{}/".format(id))
    # tabs = offer.tabs.all() 

def delete_slot(request, id):
    object = get_object_or_404(Slots, id=id)
    unit = object.unit
    object.delete()
    return redirect("/offer/tabs/units/configuration/{}/".format(unit.pk))

def delete_unit(request, id):
    object = get_object_or_404(TabUnits, id=id)
    tab = object.tab
    object.delete()
    return redirect("/offer/tabs/units/{}/".format(tab.pk))

def delete_tab(request, id):
    object = get_object_or_404(Tabs, id=id)
    offer = object.offer
    object.delete()
    return redirect("/offer/tabs/{}/".format(offer.pk))

def delete_offer(request, id):
    object = get_object_or_404(Offers, id=id)
    object.delete()
    return redirect("/offer/")

def download_offer(request,id):

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Datos'

    offer = Offers.objects.get(id=id)
    tabs = offer.tabs.all()
    units = TabUnits.objects.filter(tab__in=tabs).select_related('tab')
    slots = Slots.objects.filter(unit__in=units).select_related('unit')
    total = 0
    
    
    sheet.cell(row=1, column=1, value='PROYECTO')
    sheet.cell(row=1, column=2, value=offer.title)
    sheet.cell(row=1, column=3, value=offer.controller)
    encabezado = ['PARAMETROS','MODELO','PRECIO','TOTAL']
    # for i,tab in enumerate(tabs,2):
    #     sheet.cell(row=2, column=i, value=tab.tab_name)


    for i,value in enumerate(encabezado,1):
        sheet.cell(row=3, column=i, value=value)

    for i,slot in enumerate(slots,4):
        total += slot.slot.sale_price
        sheet.cell(row=i, column=1, value=slot.slot.product_name)
        sheet.cell(row=i, column=2, value=slot.slot.model)
        sheet.cell(row=i, column=3, value=slot.slot.sale_price)
        
    sheet.cell(row=4, column=4, value=total)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=datos.xlsx'

    workbook.save(response)
    
    return response
    # return redirect('/offer/')
    

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
                item_exist.height = float(value['height'].replace("px",""))
                item_exist.save()
            else:
                dashboard = get_object_or_404(Dasboard, id=int(data['dashboard_id']))                         
                new_item = Items(id_code=value['id_code'],x=value['x'],y=value['y'],width =float(value['width'].replace("px","")),height=float(value['height'].replace("px","")), img=img_obj, dashboard= dashboard )
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
    

def create_page(request,id):
    if request.method == 'GET':
        project = get_object_or_404(Project,id=id)
        pages_project = project.dashboards.all()
        # page = Dasboard.objects.all()
        paginator = Paginator(pages_project, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'createpage.html',{'page_obj': page_obj, 'form':CreatePage()})
    else:
        project = Project.objects.get(id=id)
        print(request.POST['name'])
        Dasboard.objects.create(name = request.POST['name'],project=project)
        return redirect(f'/createpage/{id}/')


def delete_page(request, id):
    object = get_object_or_404(Dasboard, id=id)
    project = object.project
    object.delete()
    return redirect(f'/createpage/{project.id}/')

def delete_item(request):
    if request.method == 'POST':
        raw_data = request.body
        print(f"desde delete_item: {raw_data}")
        body_unicode = raw_data.decode('utf-8')
        data = json.loads(body_unicode)
        try:
            item_exist = Items.objects.get(id_code = data['id_code'])
        except ObjectDoesNotExist:
            item_exist = None
        if item_exist:
            item_exist.delete()
        else:
            labels = get_object_or_404(Labels,id_code=data['id_code'])
            labels.delete()
        return JsonResponse({'mensaje': 'eliminado con éxito!'})