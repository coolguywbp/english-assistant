from django.contrib import admin

from . import models

@admin.register(models.Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'date_time', 'student', 'is_trial', 'is_interview', ]