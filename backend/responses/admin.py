import os, json
import requests
from django.contrib import admin
from django_object_actions import DjangoObjectActions

from . import models
# Register your models here.
class IntentAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['intent', 'examples']
    list_editable = ['examples']
    
    def rebuild_rasa(self, request, obj):
        print('Sending requiest to rebuild Rasa')
        response = requests.get('http://172.17.0.1:9000/rebuild_rasa')
        return response.content

    rebuild_rasa.label = 'Rebuild Rasa'
    rebuild_rasa.short_description  = 'Press to train new model'

    changelist_actions  = ('rebuild_rasa', )

admin.site.register(models.Intent, IntentAdmin)

@admin.register(models.Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['intent', 'response_ru', 'response_en']
    list_editable = ['response_ru', 'response_en']

@admin.register(models.Chatlog)
class ChatlogAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'action', 'content']