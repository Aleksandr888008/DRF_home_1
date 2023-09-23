from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from education.models import Course, Lesson, Subscription
from users.models import User


# Create your tests here.
class LessonTestCase(APITestCase):
    """Тестирование CRUD уроков"""

    def setUp(self) -> None:
        """Подготовка данных для тестирования"""

        self.user = User.objects.create(email='test@mail.ru', is_staff=True, is_superuser=True)
        self.client.force_authenticate(self.user)
        self.course = Course.objects.create(name='test', owner=self.user)
        self.lesson = Lesson.objects.create(name='test', course=self.course, owner=self.user)

    def test_list_lesson(self):
        """Тестирование вывода списка уроков"""
        response = self.client.get(reverse('education:lesson-list'))
        # print(response.json())
        # Проверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)

        #  Проверка корректности данных
        self.assertEquals(response.json(),
                          {'count': 1, 'next': None, 'previous': None,
                           'results': [
                               {'id': self.lesson.pk,
                                'video_link': None,
                                'name': self.lesson.name,
                                'description': None,
                                'preview': None,
                                'course': self.course.pk,
                                'owner': self.user.pk}
                           ]})

    def test_create_lesson(self):
        """Тестирование создания урока"""
        data = {"name": 'test2', 'video_link': 'https://www.youtube.com/', "course": self.course.pk}
        response = self.client.post(reverse('education:lesson-create'), data=data)
        # print(response.json())
        # Проверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_201_CREATED)
        #  Проверка корректности данных
        # print(Lesson.objects.all())
        # print(Lesson.objects.all().count())
        self.assertEquals(Lesson.objects.all().count(), 2)

        # Проверка подстановки по умолчанию текущего пользователя
        self.assertEquals(response.json().get("owner"), self.user.pk)

    def test_retrieve_lesson(self):
        """Тестирование вывода данных по отдельному уроку"""
        response = self.client.get(reverse('education:lesson-get', args=[self.lesson.pk]))
        # print(response.json())
        # Проверка статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)
        #  Проверка корректности данных
        self.assertEquals(response.json(),
                          {'id': self.lesson.pk,
                           'video_link': None,
                           'name': self.lesson.name,
                           'description': None,
                           'preview': None,
                           'course': self.course.pk,
                           'owner': self.user.pk})

    def test_update_lesson(self):
        """Тестирование обновления урока"""
        data = {"name": 'test3'}
        response = self.client.patch(reverse('education:lesson-update', args=[self.lesson.pk]), data=data)
        # print(response.json())
        # Проверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)

        # Проверка подстановки по умолчанию текущего пользователя
        self.assertEquals(response.json().get("name"), "test3")

    def test_delete_lesson(self):
        """Тестирование удаления урока"""

        response = self.client.delete(reverse('education:lesson-delete', args=[self.lesson.pk]))

        # Проверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_204_NO_CONTENT)

        # self.assertEquals(Lesson.objects.all().count(), 0)


class SubscriptionTestCase(APITestCase):
    """Тестирование Subscription"""

    def setUp(self) -> None:
        """Подготовка данных для тестирования"""

        self.user = User.objects.create(email='test@mail.ru', is_staff=True, is_superuser=True)
        self.client.force_authenticate(self.user)
        self.course = Course.objects.create(name='test', owner=self.user)
        self.subscription = Subscription.objects.create(course=self.course, is_active=True)

    def test_list_subscription(self):
        """Тестирование вывода списка подписок"""
        response = self.client.get(reverse('education:subscription_list'))
        # print(response.json())
        # Проверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)
        #  Проверка корректности данных
        self.assertEquals(response.json(),
                          [{'id': self.subscription.pk,
                            'is_active': True,
                            'user': None,
                            'course': self.course.pk}])

    def test_create_subscription(self):
        """Тестирование создания подписки"""
        data = {"course": self.course.pk, 'is_active': True}
        response = self.client.post(reverse('education:subscription_create'), data=data)
        # print(response.json())
        # Проверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_201_CREATED)

        #  Проверка корректности данных
        self.assertEquals(response.json(),
                          {'id': 2,
                           'is_active': True,
                           'user': self.user.pk,
                           'course': self.course.pk})

    def test_delete_subscription(self):
        """Тестирование удаления подписки"""

        response = self.client.delete(reverse('education:subscription_delete', args=[self.subscription.pk]))

        # Проверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_204_NO_CONTENT)