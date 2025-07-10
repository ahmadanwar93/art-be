from django.core.management.base import BaseCommand
from apps.inbound.factories import InboundTransactionFactory
from apps.outbound.factories import OutboundTransactionFactory
from apps.transfers.factories import WarehouseTransferFactory

class Command(BaseCommand):
    help = 'Seed transaction models with fake data'

    def handle(self, *args, **options):
        self.stdout.write('Starting to seed transaction models...')
        
        # Create inbound transactions
        self.stdout.write('Creating inbound transactions...')
        for i in range(20):
            transaction = InboundTransactionFactory()
            self.stdout.write(f'Created inbound transaction: {transaction.product.name} - {transaction.quantity}')
        
        # Create outbound transactions
        self.stdout.write('Creating outbound transactions...')
        for i in range(20):
            transaction = OutboundTransactionFactory()
            self.stdout.write(f'Created outbound transaction: {transaction.product.name} - {transaction.quantity}')
        
        # Create warehouse transfers
        self.stdout.write('Creating warehouse transfers...')
        for i in range(20):
            transfer = WarehouseTransferFactory()
            self.stdout.write(f'Created transfer: {transfer.product.name} from {transfer.from_warehouse.name} to {transfer.to_warehouse.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully seeded all transaction models!')
        ) 