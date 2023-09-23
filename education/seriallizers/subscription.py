from rest_framework import serializers

from education.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Сериализатор представление модели Subscription """

    class Meta:
        model = Subscription
        fields = '__all__'
