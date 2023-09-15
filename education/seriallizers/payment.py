from rest_framework import serializers

from education.models import Payment
from education.seriallizers.course import CourseSerializer
from education.seriallizers.lesson import LessonSerializer


class PaymentSerializer(serializers.ModelSerializer):
    paid_course = CourseSerializer(many=True, read_only=True)
    paid_lesson = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
