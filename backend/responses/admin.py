import os, json
import requests
from django.contrib import admin
from django_object_actions import DjangoObjectActions

from . import models
# Register your models here.
class IntentAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['intent', 'examples']
    list_editable = ['examples']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        print('Sending requiest to rebuild Rasa')
        requests.get('http://172.17.0.1:9000/rebuild_rasa')

admin.site.register(models.Intent, IntentAdmin)

@admin.register(models.Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['intent', 'response_ru', 'response_en']
    list_editable = ['response_ru', 'response_en']

@admin.register(models.Chatlog)
class ChatlogAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'action', 'content']