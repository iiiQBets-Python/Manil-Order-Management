# Generated by Django 5.1.4 on 2025-01-08 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manil_app', '0005_manil_order_details_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client_order_details',
            old_name='total',
            new_name='total_base',
        ),
        migrations.RenameField(
            model_name='manil_order_details',
            old_name='total',
            new_name='total_base',
        ),
    ]
