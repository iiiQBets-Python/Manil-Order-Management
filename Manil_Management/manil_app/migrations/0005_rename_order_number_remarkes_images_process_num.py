# Generated by Django 4.2.7 on 2024-11-22 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manil_app', '0004_order_tickets_process_num'),
    ]

    operations = [
        migrations.RenameField(
            model_name='remarkes_images',
            old_name='order_number',
            new_name='process_num',
        ),
    ]