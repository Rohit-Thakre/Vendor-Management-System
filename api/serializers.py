from rest_framework import serializers
from .models import Vendor, Purchase_Order, Historical_Performance

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase_Order
        fields = '__all__'
        


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historical_Performance
        fields = '__all__'


class Performance_serializer(serializers.ModelSerializer): 
    class Meta: 
        model = Vendor
        fields = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']

class AckSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Purchase_Order
        fields = ['ack_date']