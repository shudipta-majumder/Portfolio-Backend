from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Set the page size here
    page_size_query_param = 'page_size'
    max_page_size = 100  # Max items per page
