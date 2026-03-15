from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from stations.models import Station
from stations.api.v1.serializers.station_serializers import StationSerializer
from porter_connect.pagination import DefaultPagination



class StationListView(APIView):

    def get(self, request):
        search = request.query_params.get("search", "").strip()

        queryset = Station .objects.all()

        #Exact station code match
        if search:
            exact_code = Station.objects.filter(stnCode__iexact=search)

            if exact_code.exists():
                queryset = exact_code
            
            else:
                #Otherwise search in name/code
                queryset = queryset.filter(
                    Q(stnName__icontains=search) | 
                    Q(stnCode__icontains=search)
                )

        # Apply pagination to final queryset
        paginator= DefaultPagination()
        page = paginator.paginate_queryset(queryset, request)

        serializer = StationSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
