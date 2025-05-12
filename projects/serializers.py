from rest_framework import serializers
from .models import Project, ProjectImage, Category

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image']

class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    contributor = serializers.StringRelatedField(many=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'category_name',
            'start_date', 'end_date', 'skills_need', 'contributor',
            'publish_date', 'live_link', 'download_file', 'status', 'images'
        ]
