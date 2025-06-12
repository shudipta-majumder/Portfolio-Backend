from rest_framework import serializers
from .models import Project, ProjectImage, Category, Profile
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
    role = serializers.SerializerMethodField()
    experience_years = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'profile_pic', 'role', 'experience_years']

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

    def get_role(self, obj):
        profile = getattr(obj, 'profile', None)
        if profile:
            return profile.role
        return None
    
    def get_experience_years(self, obj):
        profile = getattr(obj, 'profile', None)
        if profile and profile.experience_years is not None:
            return profile.experience_years
        return None
   
class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    contributor = serializers.SerializerMethodField()
    category_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'category_names',
            'start_date', 'end_date', 'skills_need', 'contributor',
            'publish_date', 'live_link', 'download_file', 'status', 'images'
        ]
    
    def get_contributor(self, obj):
        request = self.context.get('request')
        contributors = obj.contributor.all()
        return ContributorSerializer(
            contributors,
            many=True,
            context={'request': request, 'project': obj}
        ).data
        
    def get_category_names(self, obj):
        return [category.name for category in obj.categories.all()]
