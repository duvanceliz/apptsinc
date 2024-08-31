from tsinc.models import *
from rest_framework import viewsets, generics
from .serializers import *


class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSelializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSelializer

class FolderListView(generics.ListAPIView):
    queryset = Folder.objects.filter(parent__isnull=True)
    serializer_class = FolderSerializerTree