# Generated by Django 4.2.7 on 2023-11-29 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_vendor_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='token',
        ),
    ]
