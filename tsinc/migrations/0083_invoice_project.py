# Generated by Django 5.0.6 on 2024-08-27 15:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0082_remission_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tsinc.project'),
        ),
    ]
