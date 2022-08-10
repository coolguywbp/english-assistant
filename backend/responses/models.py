from django.utils import timezone
from django.db import models

# Create your models here.
class Intent(models.Model):
    intent = models.CharField(verbose_name="Интент", max_length=100)
    examples = models.TextField(verbose_name="Примеры", blank=True)

    def __str__(self):
        return self.intent

class Response(models.Model):
    intent = models.OneToOneField(Intent, verbose_name="Интент", on_delete=models.CASCADE, primary_key=True)
    response_ru = models.TextField(verbose_name="Ответ(RU)")
    response_en = models.TextField(verbose_name="Ответ(EN)")

class Chatlog(models.Model):
    user = models.CharField(verbose_name="Пользователь", max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    action = models.CharField(verbose_name="Тип действия", max_length=100)
    content = models.CharField(verbose_name="Содержание", max_length=100)