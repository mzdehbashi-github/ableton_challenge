from django.utils import timezone
import factory

from user_management.models.email_confirmation import EmailConfirmation
from user_management.tests.factories.user import UserFactory


class EmailConfirmationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = EmailConfirmation
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory)
    code = factory.Faker('random_int', min=100, max=999)
    expires_at = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(hours=1))
