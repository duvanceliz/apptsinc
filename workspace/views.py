from django.shortcuts import render, redirect, get_list_or_404

from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

def staff_required(user):
    return user.is_staff

def folder_tree_func():

    root_folders =  Folder.objects.filter(parent__isnull=True)

    def get_subfolders(folder):
        """Función recursiva para obtener las subcarpetas."""
        subfolders = folder.children.all()
        return [{'folder': sub, 'subfolders': get_subfolders(sub)} for sub in subfolders]
    
    # Construir la estructura de árbol
    folder_tree = [{'folder': folder, 'subfolders': get_subfolders(folder)} for folder in root_folders]

    return folder_tree


@login_required
def overview(request):
    

    folder_tree = folder_tree_func()

    is_staff = staff_required(request.user)
    
    context = {
        'folder_tree': folder_tree, 
        'is_staff':is_staff 
    }

    return render(request,"workspace.html",context)

def overview_folder(request,name):
    folder = Folder.objects.filter(name = name).first()
    
    folder_tree = folder_tree_func()
    is_staff = staff_required(request.user)
    context = {
        'folder_tree': folder_tree, 
        'is_staff':is_staff 
    }
    
    return render(request,'overview_folder.html',context)
