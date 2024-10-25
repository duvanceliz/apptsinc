# middleware.py
from django.utils.deprecation import MiddlewareMixin
from .models import Activity,PurcharseOrder



class AuditLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Guardar el usuario actual en la sesión
        if request.user.is_authenticated:
            request.audit_user = request.user
        else:
            request.audit_user = None

    def process_response(self, request, response):

        # Comprobar si es una acción POST (crear o actualizar)
        if request.method == 'POST' and hasattr(request, 'audit_user'):
            # Extraer información sobre la acción
            if 'create' in request.path:
            # Registrar en el log
                Activity.objects.create(
                    usersession=request.audit_user,
                    action='created',
                    model=request.path  # Cambiar según el modelo
                )
            if 'edit' in request.path:
                Activity.objects.create(
                        usersession=request.audit_user,
                        action='updated',
                        model=request.path  # Cambiar según el modelo
                    )
        else:
            if 'delete' in request.path:
                Activity.objects.create(
                        usersession=request.audit_user,
                        action='deleted',
                        model=request.path  # Cambiar según el modelo
                    )

               
        return response 
    
