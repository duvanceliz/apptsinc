# Generated by Django 5.0.6 on 2024-08-15 20:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0058_alter_remission_order_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='observation',
            field=models.TextField(null=True, validators=[django.core.validators.MaxLengthValidator(500)]),
        ),
    ]