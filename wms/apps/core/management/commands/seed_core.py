from django.core.management.base import BaseCommand
from apps.core.factories import (
    WarehouseFactory, SupplierFactory, CustomerFactory, 
    ProductFactory, UserFactory, FileAttachmentFactory
)
from apps.core.models import Warehouse, User

class Command(BaseCommand):
    help = 'Seed core models with fake data'

    def handle(self, *args, **options):
        self.stdout.write('Starting to seed core models...')
        
        # Step 1: Create warehouses first
        self.stdout.write('Creating warehouses...')
        warehouses = []
        for i in range(5):
            warehouse = WarehouseFactory()
            warehouses.append(warehouse)
            self.stdout.write(f'Created warehouse: {warehouse.name}')
        
        # Step 2: Create suppliers
        self.stdout.write('Creating suppliers...')
        for i in range(20):
            supplier = SupplierFactory()
            self.stdout.write(f'Created supplier: {supplier.name}')
        
        # Step 3: Create customers
        self.stdout.write('Creating customers...')
        for i in range(20):
            customer = CustomerFactory()
            self.stdout.write(f'Created customer: {customer.name}')
        
        # Step 4: Create products
        self.stdout.write('Creating products...')
        for i in range(50):
            product = ProductFactory()
            self.stdout.write(f'Created product: {product.name}')
        
        # Step 5: Create users and ensure all warehouses have at least one user
        self.stdout.write('Creating users...')
        
        # First, assign one user to each warehouse
        for i, warehouse in enumerate(warehouses):
            user = UserFactory(warehouse=warehouse)
            self.stdout.write(f'Created user: {user.username} assigned to {warehouse.name}')
        
        # Then create remaining users (10 total - 5 already created = 5 more)
        for i in range(5):
            user = UserFactory()  # This will randomly assign to existing warehouses
            self.stdout.write(f'Created user: {user.username}')
        
        # Step 6: Create some file attachments
        self.stdout.write('Creating file attachments...')
        for i in range(10):
            attachment = FileAttachmentFactory()
            self.stdout.write(f'Created file attachment: {attachment.filename}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully seeded core models!')
        ) 