from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Создание суперюзера"""
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@mail.ru',
            first_name='Admin',
            last_name='SuperUser',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('123qwe456asd')
        user.save()
