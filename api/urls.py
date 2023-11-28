from django.urls import path
from .views import VendorView, PurchaseOrderView, Performance, Ack

urlpatterns = [
    path('vendors/', VendorView.as_view(), name='vendors_list'),  # Endpoint for getting all vendors and creating a new one
    path('vendors/<int:id>/', VendorView.as_view(), name='vendor_detail'),  # Endpoint for getting, updating, or deleting a specific vendor
    
    path('vendors/<int:id>/performance/', Performance, name='performance'),

    path('purchase_orders/', PurchaseOrderView.as_view(), name='purchase_orders_list'),
    path('purchase_orders/<int:id>/', PurchaseOrderView.as_view(), name='purchase_order_detail'),
   
    path('purchase_orders/<int:id>/acknowledge/',Ack, name='Ack'),
]

