# Generated by Django 5.1.4 on 2025-01-09 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manil_app', '0007_alter_client_order_details_total_base_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='order_number',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
