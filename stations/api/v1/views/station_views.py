from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from stations.models import Station
from stations.api.v1.serializers.station_serializers import StationSerializer
from porter_connect.pagination import DefaultPagination
from django.conf import settings



class StationListView(APIView):

    def get(self, request):
        try:
            search = request.query_params.get("search", "").strip()

            queryset = Station .objects.all()

            #Exact station code match
            if search:
                exact_code = Station.objects.filter(stn_code__iexact=search)

                if exact_code.exists():
                    queryset = exact_code
                
                else:
                    #Otherwise search in name/code
                    queryset = queryset.filter(
                        Q(stn_name__icontains=search) | 
                        Q(stn_code__icontains=search)
                    )

            # Apply pagination to final queryset
            paginator= DefaultPagination()
            page = paginator.paginate_queryset(queryset, request)

            serializer = StationSerializer(page, many=True)

            return paginator.get_paginated_response(serializer.data)
        
        except Exception as error:
            response = {
                "success": False,
                "message": "Something went wrong"
            }
            if settings.DEBUG:
                response["error"] = str(error)
                
            return Response(
                response,
                status=status.HTTP_400_BAD_REQUEST
            )
