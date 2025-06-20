# Generated by Django 5.2.1 on 2025-06-03 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_profile_project_profile_role_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='profile',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='profile',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='profiles', to='projects.project'),
        ),
        migrations.RemoveField(
            model_name='profile',
            name='project',
        ),
    ]
