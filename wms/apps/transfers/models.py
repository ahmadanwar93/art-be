from django.db import models

class WarehouseTransfer(models.Model):
    REASON_CHOICES = [
        ('rebalance', 'Stock Rebalancing'),
        ('demand', 'Demand Fulfillment'),
        ('consolidation', 'Consolidation'),
        ('emergency', 'Emergency'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)
    from_warehouse = models.ForeignKey('core.Warehouse', on_delete=models.CASCADE, related_name='outbound_transfers')
    to_warehouse = models.ForeignKey('core.Warehouse', on_delete=models.CASCADE, related_name='inbound_transfers')
    quantity = models.PositiveIntegerField()
    # For MVP, the value is assumed to not change
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    notes = models.TextField(blank=True)
    shipped_by = models.ForeignKey('core.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Transfer {self.product.sku}: {self.from_warehouse.code} -> {self.to_warehouse.code}"

