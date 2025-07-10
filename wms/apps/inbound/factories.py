import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import InboundTransaction
from apps.core.models import Product, Warehouse, Supplier, User

fake = Faker()

class InboundTransactionFactory(DjangoModelFactory):
    class Meta:
        model = InboundTransaction
    
    product = factory.LazyFunction(lambda: Product.objects.order_by('?').first())
    warehouse = factory.LazyFunction(lambda: Warehouse.objects.order_by('?').first())
    supplier = factory.LazyFunction(lambda: Supplier.objects.order_by('?').first())
    quantity = factory.LazyFunction(lambda: fake.random_int(min=1, max=100))
    unit_cost = factory.LazyFunction(lambda: fake.pydecimal(left_digits=4, right_digits=2, positive=True))
    expected_date = factory.LazyFunction(lambda: fake.future_date())
    received_date = factory.LazyFunction(lambda: fake.past_date())
    status = factory.Iterator(['pending', 'received', 'cancelled'])
    notes = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))
    received_by = factory.LazyFunction(lambda: User.objects.order_by('?').first()) 