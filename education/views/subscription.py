from rest_framework import generics

from education.models import Subscription
from education.seriallizers.subscription import SubscriptionSerializer

from education.tasks import send_message

"""Представление CRUD для модели Подписка"""


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """ Создание пидписки """
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        """Автоматическое сохранение владельца при создании нового объекта"""
        new_subscription = serializer.save()
        new_subscription.user = self.request.user
        new_subscription.save()


class SubscriptionListAPIView(generics.ListAPIView):
    """ Просмотр всех подписок """
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    """ Обновление подписки """
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        send_message.delay()


class SubscriptionRetrieveAPIView(generics.RetrieveAPIView):
    """ Просмотр одной подписки """
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionDeleteAPIView(generics.DestroyAPIView):
    """ Удаление подписки """
    queryset = Subscription.objects.all()
