# Generated by Django 5.0.6 on 2024-10-23 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0119_task_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='percent_completed',
        ),
        migrations.RemoveField(
            model_name='task',
            name='priority',
        ),
    ]
