# Generated by Django 5.0.6 on 2024-05-18 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0010_alter_project_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='approved',
            field=models.CharField(default=None, max_length=200),
        ),
    ]