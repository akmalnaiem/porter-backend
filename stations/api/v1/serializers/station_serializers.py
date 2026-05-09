from rest_framework import serializers
from stations.models import Station

class StationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Station
        fields = [
            "id",
            "stn_code",
            "stn_name",
            "stn_city"
        ]