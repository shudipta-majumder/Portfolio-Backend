from django.contrib import admin
from .models import Project, ProjectImage, Category, Profile, RequestLog

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1  # Number of empty forms to display

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_categories', 'start_date', 'end_date', 'status', 'publish_date')
    list_filter = ('categories', 'status', 'publish_date')
    search_fields = ('title', 'description', 'skills_need', 'contributor')
    date_hierarchy = 'publish_date'
    inlines = [ProjectImageInline] 
    
    def get_categories(self, obj):
        return ", ".join([cat.name for cat in obj.categories.all()])
    get_categories.short_description = 'Categories'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    
admin.site.register(Profile)

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'user', 'path', 'method', 'browser', 'os', 'accessed_at')
    list_filter = ('ip_address', 'accessed_at', 'os', 'browser', 'device_type', 'method')
    search_fields = ('ip_address', 'user_agent', 'path', 'user__username')