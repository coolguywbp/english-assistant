from django.shortcuts import render
from django.http import HttpResponseNotFound
from rest_framework.decorators import action
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from . import models
# Create your views here.
class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Call
        fields = '__all__'

class CallViewSet(viewsets.ModelViewSet):
    serializer_class = CallSerializer
    queryset = models.Call.objects.all()