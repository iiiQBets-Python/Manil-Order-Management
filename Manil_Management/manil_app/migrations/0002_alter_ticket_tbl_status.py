# Generated by Django 4.2.7 on 2024-10-29 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manil_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket_tbl',
            name='status',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
