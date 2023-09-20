from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Создание пользователя с флагом if_staff = False"""
    def handle(self, *args, **options):
        user = User.objects.create(
            email='owner@mail.ru',
            name='owner',
            is_staff=False,
            is_superuser=False

        )

        user.set_password('654321')
        user.save()
