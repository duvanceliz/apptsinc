# Generated by Django 5.0.6 on 2024-09-02 13:34

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsinc', '0092_remission_contruction_site_remission_supplier'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tsinc.invoice')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tsinc.purcharseorder')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tsinc.product')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tsinc.project')),
                ('remission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tsinc.remission')),
                ('usersession', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
