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

            vendor_name = request.data.get('vendor')
            vendor_obj = Vendor.objects.filter('name'== vendor_name).first()

            vendor_po_list = Purchase_Order.objects.filter(vendor=vendor_obj)
            sum = 0
            on_time_delivery = 0

            for x in vendor_po_list: 
                sum += x.quality_rating
                if x.delivery_date >= x.issue_date: 
                    on_time_delivery += 1



            if purchase_order_serializer.is_valid():
                purchase_order_serializer.save()
                if purchase_order_serializer.data.status == "completed":
                    vendor_obj.quality_rating_avg =  sum / vendor_po_list.count()
                    vendor_obj.on_time_delivery_rate = on_time_delivery / vendor_po_list.count()

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

@api_view(('GET',))
def Ack(request, id):
    if request.method == "POST":
        try: 
            po = Purchase_Order.objects.get(id=id)
            serializer = AckSerializer(po, data=request.data)

            vendor_id = serializer.data.get('vendor')
            vendor = Vendor.objects.get(id=vendor_id)
            all_po_of_vendor = Purchase_Order.objects.filter(vendor=vendor)

            
            diff  = 0
            for po in all_po_of_vendor: 
                diff += po.issue_date - serializer.data.get('acknowledgment_date')
            
            vendor.average_response_time = diff / all_po_of_vendor.count()
            vendor.save()

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        except: 
            return Response({'msg': 'No data associated with this id'}, status=status.HTTP_404_NOT_FOUND)

    else: 
        return Response({'msg': 'only post method allowed'}, status=status.HTTP_403_FORBIDDEN)

