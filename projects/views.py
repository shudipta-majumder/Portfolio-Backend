from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Project, Category
from .serializers import ProjectSerializer, CategorySerializer
from django.http import JsonResponse
from django.http import Http404
from portfolio.pagination import StandardResultsSetPagination
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json

# 1. List API
class ProjectListAPIView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({
                "code": 404,
                "message": "No projects found.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND) 

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "code": 200,
            "message": "Successfully retrieved projects.",
            "data": serializer.data
        })

# 2. Retrieve Single Project API
class ProjectRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        try:
            project = self.get_object()  # May raise Http404
            serializer = self.get_serializer(project)
            return Response({
                "code": 200,
                "message": "Successfully retrieved project.",
                "data": serializer.data
            })
        except (NotFound, Http404):
            return Response({
                "code": 404,
                "message": "Project not found.",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "code": 500,
                "message": "An error occurred while retrieving the project.",
                "data": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 3. Category-wise Filter API
class ProjectByCategoryAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        try:
            category_id = self.kwargs['category_id']
            queryset = Project.objects.filter(categories__id=category_id)
            if not queryset.exists():
                raise NotFound(detail="No projects found for the given category.")
            return queryset
        except NotFound as e:
            raise e
        except Exception as e:
            raise Exception(f"An error occurred while filtering by category: {str(e)}")
    
    def get(self, request, *args, **kwargs):
        try:
            projects = self.get_queryset()
            page = self.paginate_queryset(projects)  # Paginate the queryset
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                serializer = self.get_serializer(projects, many=True)
                return Response({
                    "code": 200,
                    "message": "Successfully retrieved projects for the category.",
                    "data": serializer.data
                })
        except NotFound:
            return JsonResponse({
                "code": 404,
                "message": "Category not found or no projects in this category.",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({
                "code": 500,
                "message": "An error occurred while filtering projects by category.",
                "data": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 4. Cetagory List
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
# 5. Send Email View
@csrf_exempt
def send_email_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"From: {name} <{email}>\n\n{message}"

        send_mail(
            subject=subject,
            message=full_message,
            from_email=email,
            recipient_list=['shudiptamazumdar@gmail.com'],
            fail_silently=False,
        )

        return JsonResponse({'message': 'Email sent successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)