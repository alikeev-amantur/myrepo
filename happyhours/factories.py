import factory
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.utils import timezone
from apps.user.models import ROLE_CHOICES
from apps.beverage.models import Category, Beverage
from apps.order.models import Order
from apps.partner.models import Establishment
from faker import Faker

User = get_user_model()
fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ['email']
        skip_postgeneration_save = True

    email = factory.Faker('email')
    name = factory.Faker('name')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18, maximum_age=65)
    is_blocked = False
    created_at = factory.LazyFunction(timezone.now)
    modified_at = factory.LazyFunction(timezone.now)
    role = factory.Faker('random_element', elements=[choice[0] for choice in ROLE_CHOICES])
    max_establishments = 1

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted if extracted else 'defaultpassword123'
        self.set_password(password)
        if create:
            self.save()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('word')


class EstablishmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Establishment

    name = factory.Faker('company')
    location = factory.LazyFunction(lambda: Point(float(fake.longitude()), float(fake.latitude())))
    description = factory.Faker('paragraph')
    phone_number = factory.Faker('phone_number')
    address = factory.Faker('address')
    owner = factory.SubFactory(UserFactory)



class BeverageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Beverage

    name = factory.Faker('word')
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    description = factory.Faker('paragraph')
    availability_status = factory.Faker('boolean')
    category = factory.SubFactory(CategoryFactory)
    establishment = factory.SubFactory(EstablishmentFactory)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    establishment = factory.SubFactory(EstablishmentFactory)
    beverage = factory.SubFactory(BeverageFactory)
    client = factory.SubFactory(UserFactory)
    order_date = factory.LazyFunction(timezone.now)
