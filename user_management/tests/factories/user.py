import factory

from user_management.models.user import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('email',)

    email = factory.Sequence(lambda n: f'email.{n}@test.com')
    password = factory.Faker('password')
    is_active = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", None)
        obj = super(UserFactory, cls)._create(model_class, *args, **kwargs)

        # ensure the raw password gets set after the initial save
        obj.set_password(password)
        obj.save()
        return obj
