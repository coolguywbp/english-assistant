from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from . import models

admin.site.unregister(Group)
admin.site.site_header = "English Assistant"
admin.site.site_title = "English Assistant Admin Panel"
admin.site.index_title = "Welcome to English Assistant Admin Panel"

User = get_user_model()

@admin.register(User)
class UserInAdmin(UserAdmin):
    """ All User Admin Model (Include Super User) """
    # The forms to add and change user instances
    search_fields = ['telegram_id', 'first_name', 'last_name']
    list_display = ['telegram_id', 'first_name', 'last_name', 'is_student', 'is_teacher', 'is_staff', 'is_superuser']
    list_filter = ['is_student', 'is_teacher', 'is_staff']
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    ordering = ('created_at',)
    filter_horizontal = ()

@admin.register(models.AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    
@admin.register(models.TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'working_time']
    
@admin.register(models.StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'last_call', 'teachers']