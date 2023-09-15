from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter

from education.models import Payment
from education.seriallizers.payment import PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["paid_course", "paid_lesson", "payment_method"]
    ordering_fields = ["date_payment", "payment_amount"]
    #filter_backends = [DjangoFilterBackend, OrderingFilter]
    #filterset_fields = ["paid_course", "paid_lesson", "payment_method"]
