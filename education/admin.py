from django.contrib import admin

from education.models import Course, Lesson, Payment, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('date_payment', 'paid_course', 'paid_lesson', 'payment_amount', 'payment_method')
    search_fields = ('user',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Админ панель. Отображение модели Подписки
    """
    list_display = ('user', 'course')
    search_fields = ('user', 'course',)
