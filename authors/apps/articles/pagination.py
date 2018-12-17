from rest_framework.pagination import LimitOffsetPagination

class PageNumbering(LimitOffsetPagination):
    default_limit = 10
    max_limit = 20
