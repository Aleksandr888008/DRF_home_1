from rest_framework import serializers

from education.models import Payment, Course
from education.seriallizers.course import CourseSerializer
from education.seriallizers.lesson import LessonSerializer


class PaymentSerializer(serializers.ModelSerializer):
    """ Сериализатор представление модели Payment """

    paid_course = CourseSerializer(many=True, read_only=True)
    paid_lesson = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentIntentCreateSerializer(serializers.Serializer):
    """Сериализатор для создания намерения платежа"""
    course_id = serializers.IntegerField()

    @staticmethod
    def validate_course_id(value):
        """ Проверяет, существует ли курс с таким ID """

        course = Course.objects.filter(id=value)
        if not course:
            raise serializers.ValidationError(f"Курса {value} не существует")
        return value


class PaymentMethodCreateSerializer(serializers.Serializer):
    """ Сериализатор для создания метода платежа """

    payment_token = serializers.CharField(max_length=300)


class PaymentIntentConfirmSerializer(serializers.Serializer):
    """Сериализатор для подтверждения платежа"""

    id_payment_intent = serializers.CharField(max_length=300)
    payment_token = serializers.CharField(max_length=300)

    @staticmethod
    def validate_id_payment_intent(value):
        """ Проверяет, существует ли курс с таким ID """

        payment = Payment.objects.filter(id_payment_intent=value).first()
        if payment.is_paid:
            raise serializers.ValidationError(f"Платеж с ID={value} уже подтвержден")
        if not payment:
            raise serializers.ValidationError(f"Созданного платежа с ID={value} не существует")
        return value
