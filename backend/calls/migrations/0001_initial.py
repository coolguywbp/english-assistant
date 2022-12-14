# Generated by Django 4.0.6 on 2022-08-08 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_datetime', models.DateTimeField(default='1900-01-01 12:00:00Z', verbose_name='Дата начала')),
                ('finish_datetime', models.DateTimeField(default='1900-01-01 12:00:00Z', verbose_name='Дата конца')),
                ('duration', models.IntegerField(default=30, verbose_name='Длительность в минутах')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.studentprofile', verbose_name='Ученик')),
                ('is_trial', models.BooleanField(default=False, verbose_name='Пробный урок')),
                ('is_interview', models.BooleanField(default=False, verbose_name='Собеседование')),
                ('is_notified', models.BooleanField(default=False, verbose_name='Уведомления отправлены')),
                ('is_finished', models.BooleanField(default=False, verbose_name='Проведен')),
                ('teacher_comment', models.CharField(blank=True, max_length=999, null=True, verbose_name='Комментарий учителя')),
                ('status', models.CharField(choices=[('Pending', 'PENDING'), ('Accepted', 'ACCEPTED'), ('Going', 'GOING'), ('Finished', 'FINISHED'), ('Canceled', 'CANCELED')], default='Pending', max_length=8, verbose_name='Статус')),
                ('accepted_teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accepted_teacher', to='users.teacherprofile')),
                ('pending_teachers', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pending_teachers', to='users.teacherprofile')),
                ('teachers_pool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teachers_pool', to='users.teacherprofile', verbose_name='Пул учителей')),
            ],
        ),
    ]
