from django.db import models
from django.core.validators import FileExtensionValidator
import uuid


class Product(models.Model):
    product_number = models.CharField(max_length=50, unique=True, editable=False)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(
        upload_to='products/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product_number} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.product_number:
            # Generate unique product number
            self.product_number = f"PROD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class Order(models.Model):
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    items = models.JSONField(default=dict)  # Store order items as JSON

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate unique order number
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
