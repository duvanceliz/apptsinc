# Generated by Django 5.0.6 on 2024-08-17 15:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0067_remissionfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remissionfile',
            name='order',
        ),
        migrations.AddField(
            model_name='remissionfile',
            name='remission',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tsinc.remission'),
        ),
    ]