from datetime import datetime, timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from education.models import Subscription
from users.models import User


@shared_task
def send_message(subscription: Subscription, user: User):
    """Отправка письма пользователям об обновлении материалов курса по подписки"""

    send_mail(
        subject="Обновление курса!",
        message=f"У курса {subscription.course} появилось обновление - {subscription.version}!",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )


@shared_task
def block_user():
    """Блокирует пользователей, которые не заходили более месяца"""

    now_date = datetime.now()
    one_month_ago = now_date - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago)
    inactive_users.update(is_active=False)
    print(inactive_users)
