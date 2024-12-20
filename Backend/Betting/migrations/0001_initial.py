# Generated by Django 5.1.4 on 2024-12-18 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BettingMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True, null=True)),
                ('updatedAt', models.DateTimeField(auto_now_add=True, null=True)),
                ('createdBy', models.CharField(blank=True, max_length=255, null=True)),
                ('updatedBy', models.CharField(blank=True, max_length=255, null=True)),
                ('isActive', models.BooleanField(blank=True, default=True, null=True)),
                ('userid', models.CharField(blank=True, max_length=255, null=True)),
                ('gameid', models.CharField(blank=True, max_length=255, null=True)),
                ('companyid', models.CharField(blank=True, max_length=255, null=True)),
                ('betfordate', models.CharField(blank=True, max_length=255, null=True)),
                ('betamount', models.CharField(blank=True, max_length=255, null=True)),
                ('betselectedoption', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ('-createdAt',),
                'abstract': False,
            },
        ),
    ]
