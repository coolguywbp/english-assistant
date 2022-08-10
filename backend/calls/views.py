import datetime, pytz
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
    
    def create(self, request):
        """Создаёт новый Call"""
        student_id = request.query_params['telegram_id']
        start_datetime = request.query_params['first_name']
        start_datetime = datetime.datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M:%S')
        start_datetime = pytz.utc.localize(new_call_datetime)
        try:
            user = models.User.objects.all().get(telegram_id=student_id)
        except models.User.DoesNotExist:        
            res = {"code": 404, "message": "User doesn't exists"}
            return Response(data=res, status=status.HTTP_404_NOT_FOUND)
        
        
        call = models.Call(
            user = user
            
        )
        serialized_call = CallSerializer(call)
        return Response(serialized_call.data)