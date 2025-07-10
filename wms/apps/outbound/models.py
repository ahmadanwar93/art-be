from django.db import models

class OutboundTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled'),
    ]

    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)
    warehouse = models.ForeignKey('core.Warehouse', on_delete=models.CASCADE)
    customer = models.ForeignKey('core.Customer', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    requested_date = models.DateField(null=True, blank=True)
    ship_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    shipped_by = models.ForeignKey('core.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Outbound {self.product.sku} - {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)

