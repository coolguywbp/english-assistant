from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import StudentProfile, TeacherProfile

class Call(models.Model):
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_datetime = models.DateTimeField(verbose_name="Дата начала", default="1900-01-01 12:00:00Z", blank=False)
    finish_datetime = models.DateTimeField(verbose_name="Дата конца", default="1900-01-01 12:00:00Z", blank=False)
    duration = models.IntegerField(verbose_name="Длительность в минутах", default=30, blank=False)
    
    # Users
    student = models.OneToOneField(StudentProfile, verbose_name=("Ученик"), on_delete=models.CASCADE, primary_key=True)
    teachers_pool = models.ForeignKey(TeacherProfile, related_name='teachers_pool', verbose_name=("Пул учителей"), on_delete=models.CASCADE)
    pending_teachers = models.ForeignKey(TeacherProfile, related_name='pending_teachers', on_delete=models.CASCADE, null=True, blank=True)
    accepted_teacher = models.ForeignKey(TeacherProfile, related_name='accepted_teacher', on_delete=models.CASCADE, null=True, blank=True)
    
    # Flags
    is_trial = models.BooleanField(verbose_name="Пробный урок", default=False)
    is_interview = models.BooleanField(verbose_name="Собеседование", default=False)
    is_notified = models.BooleanField(verbose_name="Уведомления отправлены", default=False)
    is_finished = models.BooleanField(verbose_name="Проведен", default=False)
    
    teacher_comment = models.CharField(verbose_name="Комментарий учителя", blank=True, null=True, max_length=999)
    
    class CallStatus(models.TextChoices):
        PENDING = 'Pending', _('PENDING')
        ACCEPTED = 'Accepted', _('ACCEPTED')
        GOING = 'Going', _('GOING')
        FINISHED = 'Finished', _('FINISHED')
        CANCELED = 'Canceled', _('CANCELED')

    status = models.CharField(
        verbose_name="Статус",
        max_length = 8,
        choices = CallStatus.choices,
        default = CallStatus.PENDING
    )