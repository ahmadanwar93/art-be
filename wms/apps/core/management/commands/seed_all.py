from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Seed all models with fake data in the correct order'

    def handle(self, *args, **options):
        self.stdout.write('Starting comprehensive seeding process...')
        
        # Step 1: Seed core models (warehouses, suppliers, customers, products, users)
        self.stdout.write('Step 1: Seeding core models...')
        call_command('seed_core')
        
        # Step 2: Seed inventory records
        self.stdout.write('Step 2: Seeding inventory records...')
        call_command('seed_inventory')
        
        # Step 3: Seed transaction models
        self.stdout.write('Step 3: Seeding transaction models...')
        call_command('seed_transactions')
        
        self.stdout.write(
            self.style.SUCCESS('All seeding completed successfully!')
        ) 