from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Project, Product, Offers, TabUnits, Tabs, Slots
from .forms import CreateProject, CreateProduct, UploadProducts, CreateOffer, CreateTab, CreateUnit, Units, SearchForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import pandas as pd
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
def dashboard(request):
    return render(request, 'dashboard.html')



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
        unit = TabUnits.objects.get(id=id)
        slots = unit.slots.all()
        products = Product.objects.all()
        paginator = Paginator(products, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        search = request.GET.get('search')
        results = []

        if search:
            results = Product.objects.filter(product_name__icontains=search)
            paginator = Paginator(results, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)  
        return render(request, 'configuration.html',{'unit': unit, 'slots':slots, 'page_obj': page_obj, 'form':SearchForm()})
    else:
        unit = TabUnits.objects.get(id=id)
        prod = Product.objects.get(id=request.POST.get('productid'))
        Slots.objects.create(slot=prod.product_name, unit= unit)
        return redirect("/offer/tabs/units/configuration/{}/".format(id))
    # tabs = offer.tabs.all()
    