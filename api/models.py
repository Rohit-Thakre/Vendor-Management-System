from django.db import models

class Vendor(models.Model): 
    name = models.CharField(max_length=150)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=150)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)  

    def __str__(self) -> str:
        return self.name

class Purchase_Order(models.Model): 
    po_number = models.CharField(max_length=150)
    vendor = models.ForeignKey(Vendor, on_delete= models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True)
    items = models.JSONField()
    quantity = models.IntegerField(default=1)
    status = models.CharField(choices=(('pending', 'pending'), ('completed', 'completed'), ('canceled', 'canceled')), max_length=10, default='pending')
    quality_rating = models.FloatField()
    issue_date = models.DateTimeField()
    ack_date = models.DateTimeField()

    def __str__(self) -> str:
        return str(self.po_number)


class Historical_Performance(models.Model): 
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self) -> str:
        return str(self.vendor)


