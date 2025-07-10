import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import Inventory
from apps.core.models import Product, Warehouse

fake = Faker()

class InventoryFactory(DjangoModelFactory):
    class Meta:
        model = Inventory
    
    product = factory.LazyFunction(lambda: Product.objects.order_by('?').first())
    warehouse = factory.LazyFunction(lambda: Warehouse.objects.order_by('?').first())
    quantity = factory.LazyFunction(lambda: fake.random_int(min=0, max=1000))
    reserved_quantity = factory.LazyFunction(lambda: fake.random_int(min=0, max=100)) 