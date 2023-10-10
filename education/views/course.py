from rest_framework import viewsets

from education.models import Course
from education.paginators import CoursePagintor
from education.permissions import IsModerator, IsOwner
from education.seriallizers.course import CourseSerializer
from education.tasks import send_message


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagintor

    def perform_update(self, serializer):
        course = serializer.save()
        send_message.delay(course.pk)

    def get_permissions(self):
        """Определение прав доступа"""
        if self.action == 'create':
            permission_classes = [IsOwner]
        elif self.action == 'list':
            permission_classes = [IsModerator | IsOwner]
        elif self.action in ('retrieve', 'update'):
            permission_classes = [IsModerator | IsOwner]
        else:  # destroy
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]
