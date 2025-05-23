from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='media/profile_pics/', blank=True, null=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} as {self.role} in {self.project.title if self.project else 'No Project'}"

    
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
    
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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
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