# Generated by Django 5.0.6 on 2024-10-23 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0118_remove_task_estimated_time_remove_task_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
