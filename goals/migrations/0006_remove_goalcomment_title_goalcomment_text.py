# Generated by Django 4.0.1 on 2022-11-11 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0005_alter_goal_category_goalcomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goalcomment',
            name='title',
        ),
        migrations.AddField(
            model_name='goalcomment',
            name='text',
            field=models.TextField(default='Описание', verbose_name='Название'),
        ),
    ]
