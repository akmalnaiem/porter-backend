from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response(
            {
                'success': True,
                'pagination': {
                    'total_records': self.page.paginator.count,
                    'total_pages': self.page.paginator.num_pages,
                    'current_page': self.page.number,
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                },
                'data': data
            },
            status=status.HTTP_200_OK
        )