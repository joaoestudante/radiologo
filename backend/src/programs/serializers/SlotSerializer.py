from rest_framework import serializers
from ..models.slot import Slot

class SlotSerializer(serializers.Serializer):
    iso_weekday = serializers.CharField(max_length=15)
    time = serializers.TimeField()

    class Meta:
        model = Slot
        fields = ['iso_weekday', 'time']
