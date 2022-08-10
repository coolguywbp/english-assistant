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

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Response
        fields = '__all__'

class ChatlogViewSet(viewsets.ModelViewSet):
    serializer_class = ChatlogSerializer
    queryset = models.Chatlog.objects.all()
    
class IntentViewSet(viewsets.ModelViewSet):
    serializer_class = IntentSerializer
    queryset = models.Intent.objects.all()

class ResponseViewSet(viewsets.ModelViewSet):
    serializer_class = ResponseSerializer
    queryset = models.Response.objects.all()
    
    def retrieve(self, request, pk=None):
        """Получает response, используя intent"""
        try:
            intent_object = models.Intent.objects.all().get(intent=pk)
        except models.Intent.DoesNotExist:
            res = {"code": 404, "message": "Intent doesn't exist"}
            return Response(data=res, status=status.HTTP_404_NOT_FOUND)
        try:
            response = models.Response.objects.all().get(pk=intent_object.pk)
        except models.Response.DoesNotExist:
            res = {"code": 404, "message": "Response doesn't exist"}
            return Response(data=res, status=status.HTTP_404_NOT_FOUND)
        serialized_response = ResponseSerializer(response)
        return Response(serialized_response.data)