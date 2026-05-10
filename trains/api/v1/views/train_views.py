from django.db import DatabaseError
from django.db.models import Q
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from trains.models import Train
from trains.api.v1.serializers.train_serializer import TrainSerialzier
from porter_connect.pagination import DefaultPagination


class TrainListAPIView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            search = request.query_params.get('search', '').strip()

            queryset = Train.objects.filter(
                is_active=True
            ).only('id', 'train_number', 'train_name')

            if search:
                queryset = queryset.filter(
                    Q(train_number__iexact=search) | 
                    Q(train_name__iexact=search)
                )
            
                serializer = TrainSerialzier(queryset, many=True)

                return Response(
                    {
                        'success': True,
                        'message': 'Train fetched successfully',
                        'data': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            
            else:
                # Apply pagination to final queryset
                paginator = DefaultPagination()
                page = paginator.paginate_queryset(queryset, request)

                serializer = TrainSerialzier(page, many=True)

                return paginator.get_paginated_response(serializer.data)
        
        except DatabaseError:
            return Response(
                {
                    'success': False,
                    'message': 'Database error occured'\
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        except Exception as e:
            response = {
                'success': False,
                'message': 'Something went wrong'
            }
            if settings.DEBUG:
                response["error"] = str(e)

            return Response(
                response,
                status=status.HTTP_400_BAD_REQUEST
            )
