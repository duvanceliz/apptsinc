# Generated by Django 5.0.6 on 2024-10-31 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0142_project_archive_tasks'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='currency',
            field=models.BooleanField(default=False),
        ),
    ]
