from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *


class Vendor_View(APIView):

    def get_list(self, request):
        vendors = Vendor.objects.all()

        vendors_serializer = VendorSerializer(vendors, many=True)

        return Response(vendors_serializer.data)
        

    def get(self, request, id): 

        try: 
            vendor = Vendor.objects.get(id = id)

            vendor_serializer = VendorSerializer(vendor)

            return Response(vendor_serializer.data)

        except: 
            pass   


    def post(self, request): 

        data = request.data
        vendor_serializer = VendorSerializer(data = data)

        if vendor_serializer.is_valid(): 
            vendor_serializer.save()

            return Response(vendor_serializer.data)
        

    def delete(self,request,id): 
        try: 
            vendor = Vendor.objects.get(id=id)
            vendor_serializer = VendorSerializer(vendor)
            vendor.delete()

            return Response(vendor_serializer.data)
        except: 
            pass


    def put(self, request, id):
        try:
            vendor = Vendor.objects.get(id=id)
            vendor_serializer = VendorSerializer(vendor, request.data)

            if vendor_serializer.is_valid(): 
                vendor_serializer.save()
                return Response(vendor_serializer.data)
        except: 
            pass



