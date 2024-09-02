from rest_framework import serializers

from .models import parcel_order


# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = parcel_order
#         fields = ['tracking_number', 'created_at']

class ItemSerializer(serializers.Serializer):
    tracking_number = serializers.CharField(max_length=16)
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S%z')