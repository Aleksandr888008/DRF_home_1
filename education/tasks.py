from datetime import datetime, timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from education.models import Subscription, Course
from users.models import User


@shared_task
def send_message(pk):

    instance = Subscription.objects.filter(course=pk)
    course = Course.objects.get(pk=pk)

    if instance:
        mail = []
        for obj in instance:
            mail.append(obj.user.email)

        send_mail(
            subject='Обновление курса!',
            message=f"У курса {course.name} появилось обновление!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=mail
        )


@shared_task
def block_user():
    """Блокирует пользователей, которые не заходили более месяца"""

    now_date = datetime.now()
    one_month_ago = now_date - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago)
    inactive_users.update(is_active=False)
    print(inactive_users)
