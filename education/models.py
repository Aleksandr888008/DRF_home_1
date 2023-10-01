from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    """Модель - курс"""
    name = models.CharField(max_length=150, verbose_name='название курса')
    preview = models.ImageField(upload_to='education/course/', verbose_name='превью курса', **NULLABLE)
    description = models.TextField(verbose_name='описание курса', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец',
                             **NULLABLE)

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ('name',)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Модель - урок"""
    name = models.CharField(max_length=150, verbose_name='название урок')
    description = models.TextField(verbose_name='описание урока', **NULLABLE)
    preview = models.ImageField(upload_to='education/lesson/', verbose_name='превью урока', **NULLABLE)
    video_link = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Название курса', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец',
                             **NULLABLE)

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Payment(models.Model):
    """Модель - платежи"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                             **NULLABLE)
    date_payment = models.DateField(auto_now_add=True, verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', **NULLABLE)
    payment_amount = models.IntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(verbose_name='способ оплаты', **NULLABLE)  # наличные или перевод на счет.

    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    id_intent = models.CharField(max_length=300, verbose_name='id_намерение платежа', **NULLABLE)
    id_method = models.CharField(max_length=300, verbose_name='id_метод платежа', **NULLABLE)
    status = models.CharField(max_length=50, verbose_name='статус платежа', **NULLABLE)

    def __str__(self):
        """Выводит информацию по оплате"""
        if self.paid_course:
            return f"{self.user} оплатил курс {self.paid_course} {self.date_payment} на сумму {self.payment_amount}"
        else:
            return f"{self.user} оплатил урок {self.paid_lesson} {self.date_payment} на сумму {self.payment_amount}"

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'


class Subscription(models.Model):
    """Модель подписка"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='подписка на курс', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='признак подписки')
    version = models.CharField(max_length=50, default=1, verbose_name='версия подписки')

    def __str__(self):
        return f'Пользователь {self.user} подписан на курс {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('user', 'course',)
