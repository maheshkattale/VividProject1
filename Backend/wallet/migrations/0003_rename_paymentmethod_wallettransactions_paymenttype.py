# Generated by Django 5.1.4 on 2024-12-22 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_wallettransactions_mobilenumber'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wallettransactions',
            old_name='paymentmethod',
            new_name='paymenttype',
        ),
    ]
