# Generated by Django 5.0.6 on 2024-05-31 03:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0024_project_sesionuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='sesionuser',
            new_name='usersesion',
        ),
    ]