# Generated by Django 5.0.6 on 2024-10-22 16:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0116_alter_task_estimated_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='estimated_time',
            field=models.TimeField(default=datetime.time(11, 22, 5, 718709)),
        ),
    ]
