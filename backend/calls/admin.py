from django.contrib import admin

from . import models

@admin.register(models.Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ['student', 'start_datetime', 'duration', 'is_trial', 'is_interview']