from django.contrib import admin
from .models import Vendor, Purchase_Order, Historical_Performance

# Register your models here

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact_details', 'vendor_code')  # Display fields in the admin interface

@admin.register(Purchase_Order)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'po_number', 'vendor', 'order_date', 'status')  # Display fields in the admin interface
    list_filter = ('status',)  # Add filters for status field

@admin.register(Historical_Performance)
class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg')  # Display fields in the admin interface
