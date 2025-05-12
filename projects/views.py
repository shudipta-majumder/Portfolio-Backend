from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Project
from .serializers import ProjectSerializer
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from portfolio.pagination import StandardResultsSetPagination

# 1. List API
class ProjectListAPIView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = StandardResultsSetPagination

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
                    "message": "Successfully retrieved projects.",
                    "data": serializer.data
                })
        except Exception as e:
            return JsonResponse({
                "code": 500,
                "message": "An error occurred while retrieving projects.",
                "data": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 2. Retrieve Single Project API
class ProjectRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'  # we will access by id

    def get(self, request, *args, **kwargs):
        try:
            project = self.get_object()  # Get the object based on `id`
            serializer = self.get_serializer(project)
            return Response({
                "code": 200,
                "message": "Successfully retrieved project.",
                "data": serializer.data
            })
        except NotFound:
            return JsonResponse({
                "code": 404,
                "message": "Project not found.",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({
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
            queryset = Project.objects.filter(category__id=category_id)
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
