from .utils import get_breadcrumbs

def breadcrumbs(request):
    return {'breadcrumbs': get_breadcrumbs(request)}