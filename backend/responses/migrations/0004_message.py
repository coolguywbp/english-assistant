# Generated by Django 4.0.6 on 2022-08-11 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('responses', '0003_alter_intent_examples'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=100, unique=True, verbose_name='Ссылка')),
                ('message_ru', models.TextField(verbose_name='Сообщение(RU)')),
                ('message_en', models.TextField(verbose_name='Сообщение(EN)')),
            ],
        ),
    ]