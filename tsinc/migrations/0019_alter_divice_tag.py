# Generated by Django 5.0.6 on 2024-07-11 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0018_divice_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='divice',
            name='tag',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
