from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Project, Product, Brand, Location
from .forms import CreateProject, CreateProduct
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
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
    paginator = Paginator(product, 5)
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