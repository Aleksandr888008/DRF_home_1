from rest_framework import serializers
from education.models import Course, Lesson
from education.seriallizers.lesson import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')

    # количества уроков для курса
    lessons_count = serializers.SerializerMethodField()

    @staticmethod
    def get_lessons_count(obj):
        lessons = Lesson.objects.filter(course=obj).all()
        if lessons:
            return lessons.count()
        return 0

    class Meta:
        model = Course
        fields = ['name', 'description', 'lessons', 'lessons_count']
