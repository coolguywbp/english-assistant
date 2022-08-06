from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    """ User Model Manager """
    def create_user(self, telegram_id, password=None, first_name=None, last_name=None, is_staff=False, is_superuser=False):
        if not telegram_id:
            raise ValueError('Users must have telegram_id')
        if not password:
            raise ValueError('User must have Password')
        if not first_name:
            raise ValueError('User must have a first name')
        if not last_name:
            raise ValueError('User must have a last name')
        user_obj = self.model(
            telegram_id = telegram_id,
            first_name = first_name,
            last_name = last_name
        )
        user_obj.set_password(password)
        user_obj.is_staff = is_staff
        user_obj.is_superuser = is_superuser
        user_obj.save(using=self._db)
        
        admin = AdminProfile(user=user_obj)
        admin.save(using=self._db)
        
    def create_staffuser(self, telegram_id, password=None, first_name=None, last_name=None):
        user = self.create_user(
            telegram_id,
            password=password,
            first_name = first_name,
            last_name = last_name,
            is_staff=True,
            is_superuser=False
        )
        return user
    def create_superuser(self, telegram_id, password=None, first_name=None, last_name=None):
        user = self.create_user(
            telegram_id,
            password=password,
            first_name = first_name,
            last_name = last_name,
            is_staff=True,
            is_superuser=True
        )        
        return user

class User(AbstractBaseUser):
    # Registration
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Telegram Data
    telegram_id = models.CharField(verbose_name="Telegram ID", unique=True, max_length=100)
    telegram_username = models.CharField(verbose_name="Telegram Username", max_length=100)
    # User Data
    first_name = models.CharField(verbose_name="Имя", blank=True, null=True, max_length=100)
    last_name = models.CharField(verbose_name="Фамилия", blank=True, null=True, max_length=100)
    timezone = models.CharField(verbose_name="Часовой пояс", blank=True, max_length=100)
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    # Flags
    is_active = models.BooleanField(verbose_name="Активен", default=True)
    is_student = models.BooleanField(verbose_name="Ученик", default=False)
    is_teacher = models.BooleanField(verbose_name="Учитель", default=False)    
    is_staff = models.BooleanField(verbose_name="Админ", default=False)
    is_superuser = models.BooleanField(verbose_name="Владелец", default=False)
    
    # Main Field for authentication
    USERNAME_FIELD = 'telegram_id'
    
    # When user create must need to fill this field
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    objects = UserManager()
    
    class Meta:
        verbose_name_plural = "Accounts"
        ordering = ('-created_at', '-updated_at', )
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_type = models.CharField(default='teacher', editable=False, max_length=7)
    balance = models.IntegerField(verbose_name="Баланс", default=0)
    is_senior = models.BooleanField(verbose_name="Старший", default=False)
    def default_working_time():
        return {
            'monday': '',
            'tuesday': '',
            'wednesday': '',
            'thursday': '',
            'friday': '',
            'saturday': '',
            'sunday': ''
        }
    
    working_time = models.JSONField(verbose_name="Рабочее время", default=default_working_time)
    class Meta:
        verbose_name_plural = "Teachers"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_type = models.CharField(default='student', editable=False, max_length=7)
    last_call = models.DateTimeField(verbose_name="Последний звонок", default="1900-01-01 12:00:00Z")
    teachers = models.ForeignKey(TeacherProfile, verbose_name=("Выбранные учителя"), on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Students"
        ordering = ('last_call',)

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_type = models.CharField(default='admin', editable=False, max_length=5)
    class Meta:
        verbose_name_plural = "Admins"