# Generated by Django 5.1.4 on 2025-01-05 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manil_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('message', models.TextField(blank=True, null=True)),
                ('is_read', models.BooleanField(default=False)),
            ],
        ),
    ]