from rest_framework import serializers
from stations.models import Station

class StationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Station
        fields = [
            "id",
            "stnCode",
            "stnName",
            "stnCity"
        ]