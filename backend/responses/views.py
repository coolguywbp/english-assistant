import datetime, pytz
from django.shortcuts import render
from django.http import HttpResponseNotFound
from rest_framework.decorators import action
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from . import models
# Create your views here.
class ChatlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chatlog
        fields = '__all__'

class IntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Intent
        fields = '__all__'

class ChatlogViewSet(viewsets.ModelViewSet):
    serializer_class = ChatlogSerializer
    queryset = models.Chatlog.objects.all()
    
class IntentViewSet(viewsets.ModelViewSet):
    serializer_class = IntentSerializer
    queryset = models.Intent.objects.all()