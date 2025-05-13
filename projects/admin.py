from django.contrib import admin
from .models import Project, ProjectImage, Category, Profile

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1  # Number of empty forms to display

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_date', 'end_date', 'status', 'publish_date')
    list_filter = ('category', 'status', 'publish_date')
    search_fields = ('title', 'description', 'skills_need', 'contributor')
    date_hierarchy = 'publish_date'
    inlines = [ProjectImageInline] 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    
admin.site.register(Profile)