import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import OutboundTransaction
from apps.core.models import Product, Warehouse, Customer, User

fake = Faker()

class OutboundTransactionFactory(DjangoModelFactory):
    class Meta:
        model = OutboundTransaction
    
    product = factory.LazyFunction(lambda: Product.objects.order_by('?').first())
    warehouse = factory.LazyFunction(lambda: Warehouse.objects.order_by('?').first())
    customer = factory.LazyFunction(lambda: Customer.objects.order_by('?').first())
    quantity = factory.LazyFunction(lambda: fake.random_int(min=1, max=50))
    unit_cost = factory.LazyFunction(lambda: fake.pydecimal(left_digits=4, right_digits=2, positive=True))
    requested_date = factory.LazyFunction(lambda: fake.past_date())
    ship_date = factory.LazyFunction(lambda: fake.past_date())
    status = factory.Iterator(['pending', 'shipped', 'cancelled'])
    notes = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))
    shipped_by = factory.LazyFunction(lambda: User.objects.order_by('?').first()) 