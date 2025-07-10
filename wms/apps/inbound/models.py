from django.db import models

class InboundTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ]

    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)
    warehouse = models.ForeignKey('core.Warehouse', on_delete=models.CASCADE)
    supplier = models.ForeignKey('core.Supplier', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    expected_date = models.DateField(null=True, blank=True)
    received_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField()
    received_by = models.ForeignKey('core.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Inbound {self.product.sku} - {self.quantity}"

    def save(self, *args, **kwargs):
        # we kinda want to save the data into database, and update the status on the go here, instead of doing controller heavy, we are model heavy
        self.total_cost = self.quantity * self.unit_cost
        # for MVP, the quantity received assumes to be the same as quantity ordered

        super().save(*args, **kwargs)
    
    