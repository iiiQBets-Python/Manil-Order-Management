# Generated by Django 4.2.7 on 2024-11-05 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manil_app', '0002_alter_ticket_tbl_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='despatch_details',
            name='remarked_by',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='despatch_details',
            name='remarked_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='despatch_details',
            name='remarks_title',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
