# Generated by Django 5.0.6 on 2024-06-13 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0040_category_subcategory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcategory',
            old_name='cotegory',
            new_name='category',
        ),
    ]