# Generated by Django 5.0.6 on 2024-09-18 13:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0103_generatedoffer_to_purcharse_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='purcharseorder',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tsinc.project'),
        ),
    ]
