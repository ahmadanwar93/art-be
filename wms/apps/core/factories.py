import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import User, Warehouse, Supplier, Customer, Product, FileAttachment

fake = Faker()

class WarehouseFactory(DjangoModelFactory):
    class Meta:
        model = Warehouse
    
    name = factory.LazyFunction(lambda: fake.company())
    code = factory.LazyFunction(lambda: fake.unique.ean8())
    address = factory.LazyFunction(lambda: fake.address())
    contact_email = factory.LazyFunction(lambda: fake.email())
    is_active = factory.LazyFunction(lambda: fake.boolean(chance_of_getting_true=80))

class SupplierFactory(DjangoModelFactory):
    class Meta:
        model = Supplier
    
    name = factory.LazyFunction(lambda: fake.company())
    email = factory.LazyFunction(lambda: fake.email())
    is_active = factory.LazyFunction(lambda: fake.boolean(chance_of_getting_true=90))

class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer
    
    name = factory.LazyFunction(lambda: fake.company())
    email = factory.LazyFunction(lambda: fake.email())
    is_active = factory.LazyFunction(lambda: fake.boolean(chance_of_getting_true=90))

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product
    
    name = factory.LazyFunction(lambda: fake.product_name())
    sku = factory.LazyFunction(lambda: fake.unique.ean13())
    description = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))
    category = factory.Iterator([choice[0] for choice in Product.CATEGORY_CHOICES])
    tags = factory.LazyFunction(lambda: fake.random_elements(
        elements=Product.TAG_CHOICES,
        length=fake.random_int(min=0, max=3),
        unique=True
    ))
    unit_cost = factory.LazyFunction(lambda: fake.pydecimal(left_digits=4, right_digits=2, positive=True))
    low_stock_threshold = factory.LazyFunction(lambda: fake.random_int(min=5, max=50))
    is_active = factory.LazyFunction(lambda: fake.boolean(chance_of_getting_true=90))

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.LazyFunction(lambda: fake.unique.user_name())
    email = factory.LazyFunction(lambda: fake.email())
    first_name = factory.LazyFunction(lambda: fake.first_name())
    last_name = factory.LazyFunction(lambda: fake.last_name())
    role = factory.Iterator(['admin', 'manager', 'operator'])
    warehouse = factory.LazyFunction(lambda: Warehouse.objects.order_by('?').first())
    is_active = True
    
    @factory.post_generation
    def set_password(self, create, extracted, **kwargs):
        if create:
            self.set_password('password')

class FileAttachmentFactory(DjangoModelFactory):
    class Meta:
        model = FileAttachment
    
    entity_type = factory.Iterator(['inbound', 'outbound'])
    entity_id = factory.LazyFunction(lambda: fake.random_int(min=1, max=100))
    filename = factory.LazyFunction(lambda: fake.file_name(extension='pdf'))
    uploaded_by = factory.LazyFunction(lambda: User.objects.order_by('?').first()) 