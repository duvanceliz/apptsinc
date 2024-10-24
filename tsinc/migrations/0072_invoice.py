# Generated by Django 5.0.6 on 2024-08-21 14:09

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0071_productfile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=100)),
                ('total_price', models.FloatField(default=0)),
                ('iva', models.FloatField(default=0)),
                ('source_retention', models.FloatField(default=0)),
                ('ica_retentiton', models.FloatField(default=0)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('usersession', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
