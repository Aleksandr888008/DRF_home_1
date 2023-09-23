from rest_framework import serializers
from education.models import Lesson
from education.validators import validator_url


class LessonSerializer(serializers.ModelSerializer):
    """ Сериализатор представление модели Lesson """

    video_link = serializers.URLField(validators=[validator_url])       # валидатор на url

    class Meta:
        model = Lesson
        fields = '__all__'
