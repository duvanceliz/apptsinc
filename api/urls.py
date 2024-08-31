
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework.documentation import include_docs_urls


router = DefaultRouter()
router.register(r'folder', FolderViewSet,'folder')
router.register(r'projects', ProjectViewSet,'project')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    # path('docs/', include_docs_urls(title = "Doc API")),
    path('api/v1/folders/', FolderListView.as_view(), name='folder-list'),

]