import json, logging
from django.shortcuts import render
from django.http import HttpResponseNotFound
from rest_framework.decorators import action
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from . import models
# Create your views here.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['pk', 'telegram_id', 'telegram_username', 'first_name', 'last_name', 'timezone', 'is_active', 'is_student', 'is_teacher', 'is_staff']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.StudentProfile
        fields = '__all__'
    def create(self, validated_data):
        user_validated_data = validated_data.pop('user', None)
        user = models.User.objects.create(**user_validated_data)        
        student = models.StudentProfile.objects.create(user=user,**validated_data)
        return student

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.TeacherProfile
        fields = '__all__'
    def create(self, validated_data):
        user_validated_data = validated_data.pop('user', None)
        user = models.User.objects.create(**user_validated_data)        
        teacher = models.TeacherProfile.objects.create(user=user,**validated_data)
        return teacher

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.AdminProfile
        fields = '__all__'
    def create(self, validated_data):
        user_validated_data = validated_data.pop('user', None)
        user = models.User.objects.create(**user_validated_data)        
        admin = models.AdminProfile.objects.create(user=user,**validated_data)
        return admin

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = models.User.objects.all()
    
    
    def create(self, request):
        """Создаёт нового User, делает его учеником и создаёт StudentProfile"""
        telegram_id = request.query_params['telegram_id']
        telegram_username = request.query_params['telegram_username']
        first_name = request.query_params['first_name']
        last_name = request.query_params['last_name']
        
        try:
            user = models.User.objects.all().get(telegram_id=telegram_id)
            res = {"code": 400, "message": "User already exists"}
            return Response(res, status=status.HTTP_200_OK)
        except models.User.DoesNotExist:        
            user = models.User(
                telegram_id = telegram_id,
                telegram_username = telegram_username,
                first_name = first_name,
                last_name = last_name,
                is_student = True,
                
            )
            student = models.StudentProfile(user=user)
            
            user.save()
            student.save()
            
            serialized_student = StudentSerializer(student)
            return Response(serialized_student.data)
    
    
    def retrieve(self, request, pk=None):
        """Получает юзеров, используя telegram_id"""
        try:
            user = models.User.objects.all().get(telegram_id=pk)
        except models.User.DoesNotExist:
            res = {"code": 404, "message": "User doesn't exists"}
            return Response(data=res, status=status.HTTP_404_NOT_FOUND)
        
        if user.is_student:
            student = models.StudentProfile.objects.all().get(user=user.pk)
            serialized_student = StudentSerializer(student)
            return Response(serialized_student.data)
        elif user.is_teacher:
            teacher = models.TeacherProfile.objects.all().get(user=user.pk)
            serialized_teacher = TeacherSerializer(teacher)
            return Response(serialized_teacher.data)
        else:
            admin = models.AdminProfile.objects.all().get(user=user.pk)
            serialized_admin = AdminSerializer(admin)
            return Response(serialized_admin.data)
    
    
    @action(methods=['post'], detail=False)
    def student_to_teacher(self, request):
        """Делает Ученика Учителем, удаляет Student Profile и создаёт Teacher Profile"""
        telegram_id = request.query_params['telegram_id']
        user = models.User.objects.all().get(telegram_id=telegram_id)
        
        if user.is_student:
            profile = models.StudentProfile.objects.all().get(user=user.pk)
            profile.delete()
            
            profile = models.TeacherProfile(user=user)
            profile.save()

            user.is_student = False
            user.is_teacher = True
            user.save()            
            
            serialized_user = UserSerializer(user)
            return Response(serialized_user.data)
        else:
            return HttpResponseNotFound()
    
    @action(methods=['post'], detail=False)
    def teacher_to_student(self, request):
        """Делает Учителя Учеником, удаляет Teacher Profile и создаёт Student Profile"""
        telegram_id = request.query_params['telegram_id']
        user = models.User.objects.all().get(telegram_id=telegram_id)
        
        if user.is_teacher:
            profile = models.TeacherProfile.objects.all().get(user=user.pk)
            profile.delete()
            
            profile = models.StudentProfile(user=user)
            profile.save()

            user.is_teacher = False
            user.is_student = True
            user.save()            
            
            serialized_user = UserSerializer(user)
            return Response(serialized_user.data)
        else:
            return HttpResponseNotFound()