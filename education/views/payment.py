from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from education.models import Payment
from education.permissions import IsModerator, IsOwner
from education.seriallizers.payment import PaymentSerializer, PaymentIntentCreateSerializer, \
    PaymentIntentConfirmSerializer
from education.services import PaymentService


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["paid_course", "paid_lesson", "payment_method"]
    ordering_fields = ["date_payment", "payment_amount"]
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_fields = ["paid_course", "paid_lesson", "payment_method"]


class PaymentCreateAPIView(generics.CreateAPIView):
    """ Создание платежа"""
    serializer_class = PaymentSerializer


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """ Просмотр одного платежа """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsModerator | IsOwner]


class PaymentIntentCreateView(generics.CreateAPIView):
    """ Создание платежного намерения """

    serializer_class = PaymentIntentCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            course_id = serializer.validated_data['course_id']
            user = self.request.user
            try:
                payment_intent = PaymentService.create_payment_intent(course_id=course_id, user=user)
                payment = Payment.objects.filter(id_payment_intent=payment_intent['id']).first()
                payment_serializer = PaymentSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentIntentConfirmView(generics.CreateAPIView):
    """ Подтверждение платежа """

    serializer_class = PaymentIntentConfirmSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            id_payment_intent = serializer.validated_data['id_payment_intent']
            payment_token = serializer.validated_data['payment_token']
            try:
                # создание метода платежа
                payment_method = PaymentService.create_payment_method(payment_token)
                # привязка метода платежа к платежному намерению
                PaymentService.connect_payment_intent_and_method(payment_method_id=payment_method["id"],
                                                                 id_payment_intent=id_payment_intent)
                # подтверждение платежа
                PaymentService.confirm_payment_intent(id_payment_intent)
                payment = Payment.objects.filter(id_payment_intent=id_payment_intent).first()
                # изменение статуса платежа на "Оплачено"
                payment.change_is_paid()
                payment_serializer = PaymentSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
