# Generated by Django 5.0.6 on 2024-07-08 13:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0005_license'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='sheet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='license', to='tsinc.sheet'),
        ),
    ]
