from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Project(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='projects')
    start_date = models.DateField()
    end_date = models.DateField()
    skills_need = models.TextField(help_text="List skills separated by commas")
    contributor = models.ManyToManyField(User, related_name='projects')
    publish_date = models.DateField()
    live_link = models.URLField(blank=True, null=True)
    download_file = models.FileField(upload_to='media/project_files/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/project_images/')

    def __str__(self):
        return f"Image for {self.project.title}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='media/profile_pics/', blank=True, null=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    experience_years = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} as {self.role}"
    
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
        
class RequestLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    user_agent = models.TextField()
    browser = models.CharField(max_length=100, blank=True)
    os = models.CharField(max_length=100, blank=True)
    device_info = models.CharField(max_length=100, blank=True)
    referer = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=100, blank=True)
    accessed_at = models.DateTimeField()

    def __str__(self):
        return f"{self.ip_address} -> {self.path} @ {self.accessed_at}"