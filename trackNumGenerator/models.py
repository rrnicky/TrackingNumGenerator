from django.db import models
# Create your models here.

class parcel_order(models.Model):
    origin_country_id = models.CharField(max_length=2)
    destination_country_id = models.CharField(max_length=2)
    weight = models.DecimalField(max_digits=10, decimal_places=3)
    order_created_at = models.DateTimeField(auto_now_add=True)
    trackingNo_created_at = models.DateTimeField(auto_now_add=True)
    customer_id = models.UUIDField()
    customer_name = models.CharField(max_length=255)
    customer_slug = models.SlugField(max_length=255)
    tracking_number = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.tracking_number