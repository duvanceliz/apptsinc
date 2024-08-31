from rest_framework import serializers
from tsinc.models import *

class FolderSelializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'


class ProjectSelializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class FolderSerializerTree (serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ['id', 'name', 'children']

    def get_children(self, obj):
        if obj.children.exists():
            return FolderSerializerTree(obj.children.all(), many=True).data
        return []

