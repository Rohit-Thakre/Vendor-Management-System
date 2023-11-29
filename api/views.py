from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Vendor
from .serializers import VendorSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Purchase_Order
from .serializers import PurchaseOrderSerializer, Performance_serializer, AckSerializer

from django.db.models import Q

class VendorView(APIView):
    def get(self, request, id=None):
        if id:
            try:
                vendor = Vendor.objects.get(id=id)
                vendor_serializer = VendorSerializer(vendor)
                return Response(vendor_serializer.data)
            except Vendor.DoesNotExist:
                return Response({'msg': 'No data associated with this id'}, status=status.HTTP_404_NOT_FOUND)
        else:
            vendors = Vendor.objects.all()
            vendors_serializer = VendorSerializer(vendors, many=True)
            return Response(vendors_serializer.data)

    def post(self, request):
        vendor_serializer = VendorSerializer(data=request.data)
        if vendor_serializer.is_valid():
            vendor_serializer.save()
            return Response(vendor_serializer.data, status=status.HTTP_201_CREATED)
        return Response(vendor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            vendor = Vendor.objects.get(id=id)
            vendor.delete()
            return Response({'msg': 'Vendor deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Vendor.DoesNotExist:
            return Response({'msg': 'No data associated with this id'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            vendor = Vendor.objects.get(id=id)
            vendor_serializer = VendorSerializer(vendor, data=request.data)
            if vendor_serializer.is_valid():
                vendor_serializer.save()
                return Response(vendor_serializer.data)
            return Response(vendor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Vendor.DoesNotExist:
            return Response({'msg': 'No data associated with this id'}, status=status.HTTP_404_NOT_FOUND)


from datetime import datetime,timedelta
# date_format = "%m/%d/%Y"
date_format = '%Y-%m-%d %H:%M:%S%z'
class PurchaseOrderView(APIView):
    def get(self, request, id=None):
        if id:
            try:
                purchase_order = Purchase_Order.objects.get(id=id)
                purchase_order_serializer = PurchaseOrderSerializer(purchase_order)
                return Response(purchase_order_serializer.data)
            except Purchase_Order.DoesNotExist:
                return Response({'msg': 'No data associated with this id'}, status=status.HTTP_404_NOT_FOUND)
        else:
            purchase_orders = Purchase_Order.objects.all()
            purchase_orders_serializer = PurchaseOrderSerializer(purchase_orders, many=True)
            return Response(purchase_orders_serializer.data)

    def post(self, request):
        purchase_order_serializer = PurchaseOrderSerializer(data=request.data)
        if purchase_order_serializer.is_valid():
            purchase_order_serializer.save()
            return Response(purchase_order_serializer.data, status=status.HTTP_201_CREATED)
        return Response(purchase_order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            purchase_order = Purchase_Order.objects.get(id=id)
            purchase_order.delete()
            return Response({'msg': 'Purchase order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Purchase_Order.DoesNotExist:
            return Response({'msg': 'No data associated with this id'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, id):
        try:
            purchase_order = Purchase_Order.objects.get(id=id)
            purchase_order_serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
            
            if purchase_order_serializer.is_valid():
                old_status = purchase_order.status
                purchase_order_serializer.save()

                new_status = purchase_order_serializer.data['status']
                if new_status == "completed":
                    vendor_name = purchase_order.vendor.name
                    vendor_obj = Vendor.objects.filter(name=vendor_name).first()

                    vendor_po_list = Purchase_Order.objects.filter(vendor=vendor_obj)
                    

                    completed_po = Purchase_Order.objects.filter(Q(vendor= vendor_obj) & Q(status='completed') )
                    completed_po_cnt = completed_po.count()
                    before_time_delivery_count = 0
                    sum_quality_rating = 0
                    # sum_average_response_time = timedelta()
                    sum_average_response_time = 0
                    for x in completed_po: 

                        issue_date = datetime.strptime(str(x.issue_date), date_format)
                        ack_date = datetime.strptime(str(x.ack_date), date_format)

                        diff = issue_date - ack_date 
                        diff = diff.total_seconds() / 3600 
                        sum_average_response_time += diff


                        if x.expected_delivery_date > x.delivery_date: 
                            before_time_delivery_count += 1
                    
                    vendor_obj.on_time_delivery_rate = before_time_delivery_count / completed_po_cnt
                    vendor_obj.quality_rating_avg = sum_quality_rating / completed_po_cnt
                    vendor_obj.average_response_time = sum_average_response_time / completed_po_cnt
                    vendor_obj.fulfillment_rate = completed_po_cnt / vendor_po_list.count()
                    vendor_obj.save()


                return Response(purchase_order_serializer.data)
            return Response(purchase_order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Purchase_Order.DoesNotExist:
            return Response({'msg': 'No data associated with this id'}, status=status.HTTP_404_NOT_FOUND)

#  GET/api/vendors/{vendor_id}/performance):
# POST /api/purchase_orders/{po_id}/acknowledge
from rest_framework.decorators import api_view
@api_view(('GET',))
def Performance(request, id):
    try:
        vendor = Vendor.objects.get(id=id) 
        serializer = Performance_serializer(vendor)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    except: 
        return Response({'msg': 'No data associated with this id'}, status=status.HTTP_404_NOT_FOUND)

@api_view(( 'POST',))
def Ack(request, id):
    if request.method == "POST":
        
        po = Purchase_Order.objects.get(id=id)
        serializer = AckSerializer(po, data=request.data)
        if serializer.is_valid():
            serializer.save()

        vendor_name = po.vendor
        vendor = Vendor.objects.get(name = po.vendor)
        all_po_of_vendor = Purchase_Order.objects.filter(vendor=vendor)

            
        sum_average_response_time = 0
        for po in all_po_of_vendor: 

            print('this working')
            issue_date = datetime.strptime(str(po.issue_date), date_format)
            ack_date = datetime.strptime(str(po.ack_date), date_format)

            diff = issue_date - ack_date 
            diff = diff.total_seconds() / 3600 
            sum_average_response_time += diff
            
        vendor.average_response_time = sum_average_response_time / all_po_of_vendor.count()
        vendor.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        # exc`ept: 
        #     return Response({'msg': 'No data associated with this id'}, status=status.HTTP_404_NOT_FOUND)

    else: 
        return Response({'msg': 'only post method allowed'}, status=status.HTTP_403_FORBIDDEN)

