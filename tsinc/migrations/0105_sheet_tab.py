# Generated by Django 5.0.6 on 2024-09-18 21:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0104_purcharseorder_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheet',
            name='tab',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tab', to='tsinc.tabs'),
        ),
    ]