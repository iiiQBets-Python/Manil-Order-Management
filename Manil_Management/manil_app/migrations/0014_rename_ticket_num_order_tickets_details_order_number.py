# Generated by Django 5.1.4 on 2025-01-15 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manil_app', '0013_order_tickets_details_order_tickets_remarks_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order_tickets_details',
            old_name='ticket_num',
            new_name='order_number',
        ),
    ]
