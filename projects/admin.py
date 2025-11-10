from django.contrib import admin
from .models import Project, ProjectImage, Category, Profile, RequestLog
from django.utils.html import format_html

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
    
# admin.site.register(Profile)

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'user', 'path', 'method', 'browser', 'os', 'accessed_at')
    list_filter = ('ip_address', 'accessed_at', 'os', 'browser', 'device_info', 'method')
    search_fields = ('ip_address', 'user_agent', 'path', 'user__username')
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'experience_years', 'profile_pic_preview')
    search_fields = ('user__username', 'role')
    
    def profile_pic_preview(self, obj):
        if obj.profile_pic:
            return format_html(
                '<img src="{}" style="height:50px;width:50px;object-fit:cover;border-radius:50%;" />',
                obj.profile_pic.url
            )
        return "-"
    profile_pic_preview.short_description = 'Profile Picture'