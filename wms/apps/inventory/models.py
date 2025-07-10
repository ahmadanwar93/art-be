from django.db import models

class Inventory(models.Model):
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)
    warehouse = models.ForeignKey('core.Warehouse', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['product', 'warehouse']

    def __str__(self):
        return f"{self.product.sku} @ {self.warehouse.code}: {self.quantity}"
    
    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity