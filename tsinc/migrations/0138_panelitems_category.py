# Generated by Django 5.0.6 on 2024-10-28 21:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0137_alter_comment_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='panelitems',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tsinc.category'),
        ),
    ]
