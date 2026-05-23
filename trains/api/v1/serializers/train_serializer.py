from rest_framework import serializers

from trains.models import Train


class TrainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Train
        fields = (
            'id',
            'train_number',
            'train_name'
        )
