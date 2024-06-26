from rest_framework.pagination import PageNumberPagination
from .constants import PAGE_SIZE, MAX_PAGE_SIZE


class CustomNumberPagination(PageNumberPagination):
    page_size = PAGE_SIZE
    page_size_query_param = "page_size"
    max_page_size = MAX_PAGE_SIZE
