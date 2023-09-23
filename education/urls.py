from django.urls import path
from rest_framework.routers import DefaultRouter

from education.apps import EducationConfig
from education.views.course import CourseViewSet
from education.views.lesson import LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView
from education.views.payment import PaymentListAPIView
from education.views.subscription import SubscriptionCreateAPIView, SubscriptionListAPIView, \
    SubscriptionRetrieveAPIView, SubscriptionDeleteAPIView

app_name = EducationConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),

    path('payment/', PaymentListAPIView.as_view(), name='payment-list'),

    path('subscriptions/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('subscriptions/', SubscriptionListAPIView.as_view(), name='subscription_list'),
    path('subscriptions/<int:pk>/', SubscriptionRetrieveAPIView.as_view(), name='subscription_retrieve'),
    path('subscriptions/delete/<int:pk>/', SubscriptionDeleteAPIView.as_view(), name='subscription_delete'),

] + router.urls
