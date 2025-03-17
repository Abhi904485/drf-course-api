from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'size'
    max_page_size = 10
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'count': self.page.paginator.count,
            'results': data
        })


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 1
    offset_query_param = 'offset'
    limit_query_param = 'limit'
    max_limit = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'count': self.limit,
            'results': data
        })
