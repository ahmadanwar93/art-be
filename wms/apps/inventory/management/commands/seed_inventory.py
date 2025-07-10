from django.core.management.base import BaseCommand
from apps.inventory.factories import InventoryFactory
from apps.core.models import Product, Warehouse

class Command(BaseCommand):
    help = 'Seed inventory records with fake data'

    def handle(self, *args, **options):
        self.stdout.write('Starting to seed inventory records...')
        
        # Create inventory records for products and warehouses
        # We'll create inventory for some products in some warehouses (not all combinations)
        products = Product.objects.all()
        warehouses = Warehouse.objects.all()
        
        # Create inventory records (mix and match approach)
        inventory_count = 0
        for product in products:
            # For each product, create inventory in 1-3 random warehouses
            num_warehouses = min(3, warehouses.count())
            selected_warehouses = warehouses.order_by('?')[:num_warehouses]
            
            for warehouse in selected_warehouses:
                inventory = InventoryFactory(product=product, warehouse=warehouse)
                inventory_count += 1
                self.stdout.write(f'Created inventory: {product.name} @ {warehouse.name}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {inventory_count} inventory records!')
        ) 