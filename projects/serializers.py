from rest_framework import serializers
from .models import Project, ProjectImage, Category
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        
class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image']

class ContributorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'profile_pic']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

    def get_profile_pic(self, obj):
        profile = getattr(obj, 'profile', None)
        if profile and profile.profile_pic:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(profile.profile_pic.url)
            return profile.profile_pic.url
        return None
    
class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    contributor = ContributorSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'category_name',
            'start_date', 'end_date', 'skills_need', 'contributor',
            'publish_date', 'live_link', 'download_file', 'status', 'images'
        ]
