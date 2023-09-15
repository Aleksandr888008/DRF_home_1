from django.core.management import BaseCommand

from education.models import Payment


class Command(BaseCommand):
    
    def handle(self, *args, **options):

        payment_list = [
            {
             'date_payment': '2022-01-01',
             'payment_amount': 50000,
             'payment_method': 'перевод на счет',
             },

            {
             'date_payment': '2023-01-01',
             'payment_amount': 10000,
             'payment_method': 'наличные',
             },
        ]

        payments_objects = []
        for payments_item in payment_list:
            payments_objects.append(Payment(**payments_item))

        Payment.objects.bulk_create(payments_objects)
