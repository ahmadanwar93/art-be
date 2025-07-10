from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # we use tuple such that the first value is database value and the second value is human readable value
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('operator', 'Operator'),
    ]
    # for now, email is optional. But maybe we will make it required later if there is a need for email notification
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='operator')
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    # For MVP, the category and tags choices are pre-defined
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('furniture', 'Furniture'),
        ('clothing', 'Clothing'),
        ('raw_materials', 'Raw Materials'),
        ('finished_goods', 'Finished Goods'),
        ('consumables', 'Consumables'),
        ('tools_equipment', 'Tools & Equipment'),
        ('office_supplies', 'Office Supplies'),
    ]

    # For reference only, will have to do validation manually later
    TAG_CHOICES = [
        'fragile', 'hazardous', 'perishable', 'bulk', 
        'imported', 'premium', 'seasonal', 'fast-moving', 'slow-moving'
    ]

    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    tags = models.JSONField(default=list, blank=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # will be used to notify us when stock falls below this level
    low_stock_threshold = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    def get_total_quantity_across_warehouses(self):
        # TODO: check import
        from apps.inventory.models import Inventory
        inventories = Inventory.objects.filter(product=self).aggregate(
            total = models.Sum('quantity')
        )['total'] or 0

        return inventories

    def get_available_quantity_across_warehouses(self):
        # TODO: put the property in Inventory
        from apps.inventory.models import Inventory
        inventories = Inventory.objects.filter(product=self)
        total_available = sum(inv.available_quantity for inv in inventories)

        return total_available
    
class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('bulk_upload', 'Bulk Upload'),
        ('transfer', 'Transfer'),
    ]

    # will be user_id in the table
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    # Similar to polymorph in Laravel
    entity_type = models.CharField(max_length=30)
    entity_id = models.PositiveIntegerField()
    # For human readable identifier
    entity_name = models.CharField(max_length=200)
    description = models.TextField()
    changes = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} {self.action} {self.entity_type} at {self.created_at}"

class FileAttachment(models.Model):
    ENTITY_CHOICES = [
        ('inbound', 'Inbound Transaction'),
        ('outbound', 'Outbound Transaction'),
    ]

    entity_type = models.CharField(max_length=20, choices=ENTITY_CHOICES)
    entity_id = models.PositiveIntegerField()
    filename = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey('core.User', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} for {self.entity_type} {self.entity_id}"




