# from .utils import get_breadcrumbs
from .models import Folder

# def breadcrumbs(request):
#     return {'breadcrumbs': get_breadcrumbs(request)}


def folder_tree(request):
    folders = Folder.objects.select_related('parent').order_by('parent_id', 'order')
    return {
        'folder_tree':folders 
    }

def get_user(request):
    return {
        'user':request.user
    }