from rest_framework import viewsets

from education.models import Course
from education.permissions import IsModerator, IsOwner
from education.seriallizers.course import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsModerator | IsOwner]
