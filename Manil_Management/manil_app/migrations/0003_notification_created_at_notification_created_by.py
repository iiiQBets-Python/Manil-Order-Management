# Generated by Django 5.1.4 on 2025-01-05 16:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manil_app', '0002_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='notification',
            name='created_by',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
