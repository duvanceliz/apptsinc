# Generated by Django 5.0.6 on 2024-10-30 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0141_file_task_delete_taskfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='archive_tasks',
            field=models.BooleanField(default=False),
        ),
    ]
