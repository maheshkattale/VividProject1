# Generated by Django 5.1.4 on 2024-12-22 11:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0003_rename_paymentmethod_wallettransactions_paymenttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallettransactions',
            name='Date',
            field=models.DateField(default=django.utils.timezone.now, null=True),
        ),
    ]
