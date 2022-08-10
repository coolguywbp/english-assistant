import os
from django.contrib import admin
from django_object_actions import DjangoObjectActions

from . import models
# Register your models here.
class IntentAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['intent', 'examples']
    list_editable = ['examples']
    
    def train_rasa(self, request, obj):
        print('Trining')
        print(os.path.dirname(os.path.abspath(__file__)))
        print(os.listdir('../rasa/data'))

    train_rasa.label = 'Train Rasa'
    train_rasa.short_description  = 'Press to train new model'

    changelist_actions  = ('train_rasa', )

admin.site.register(models.Intent, IntentAdmin)

@admin.register(models.Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['intent', 'response_ru', 'response_en']
    list_editable = ['response_ru', 'response_en']

@admin.register(models.Chatlog)
class ChatlogAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'action', 'content']