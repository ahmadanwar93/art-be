import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import WarehouseTransfer
from apps.core.models import Product, Warehouse, User

fake = Faker()

class WarehouseTransferFactory(DjangoModelFactory):
    class Meta:
        model = WarehouseTransfer
    
    product = factory.LazyFunction(lambda: Product.objects.order_by('?').first())
    from_warehouse = factory.LazyFunction(lambda: Warehouse.objects.order_by('?').first())
    to_warehouse = factory.LazyFunction(lambda: Warehouse.objects.exclude(id=factory.SelfAttribute('from_warehouse.id')).order_by('?').first())
    quantity = factory.LazyFunction(lambda: fake.random_int(min=1, max=50))
    reason = factory.Iterator(['rebalance', 'demand', 'consolidation', 'emergency', 'other'])
    notes = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))
    shipped_by = factory.LazyFunction(lambda: User.objects.order_by('?').first())
    status = factory.Iterator(['pending', 'completed', 'cancelled']) 