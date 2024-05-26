from django.urls import reverse

def get_breadcrumbs(request):
    path = request.path.strip('/').split('/')
    breadcrumbs = []
    for i in range(len(path)):
        breadcrumb_path = '/'.join(path[:i + 1])
        breadcrumb_name = path[i].replace('-', ' ').title()  # Puedes personalizar cómo se muestra el nombre
        breadcrumbs.append((breadcrumb_name, '/' + breadcrumb_path))
    return breadcrumbs