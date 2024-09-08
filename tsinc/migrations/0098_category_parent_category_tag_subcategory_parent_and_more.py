# Generated by Django 5.0.6 on 2024-09-05 16:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0097_project_closing_date_project_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='tsinc.category'),
        ),
        migrations.AddField(
            model_name='category',
            name='tag',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='tsinc.subcategory'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='tag',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
