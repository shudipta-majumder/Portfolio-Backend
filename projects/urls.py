# urls.py
from django.urls import path
from .views import ProjectListAPIView, ProjectRetrieveAPIView, ProjectByCategoryAPIView, CategoryListAPIView, send_email_view

urlpatterns = [
    path('projects/', ProjectListAPIView.as_view(), name='project-list'),
    path('projects/<int:id>/', ProjectRetrieveAPIView.as_view(), name='project-detail'),
    path('projects/category/<int:category_id>/', ProjectByCategoryAPIView.as_view(), name='project-by-category'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('send-email/', send_email_view, name='send-email'),
]
