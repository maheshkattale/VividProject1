# Generated by Django 5.1.4 on 2024-12-22 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0005_remove_wallettransactions_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallettransactions',
            name='date',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='wallettransactions',
            name='time',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
