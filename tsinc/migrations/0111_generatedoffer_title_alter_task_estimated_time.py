# Generated by Django 5.0.6 on 2024-10-12 14:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0110_product_measure_alter_task_estimated_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatedoffer',
            name='title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='estimated_time',
            field=models.TimeField(default=datetime.time(9, 6, 0, 644795)),
        ),
    ]
