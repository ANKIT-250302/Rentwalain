# Generated by Django 5.1.4 on 2025-01-08 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0002_landlordprofile_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landlordprofile',
            name='profilepic',
            field=models.ImageField(blank=True, default='profiles/unnamed.webp', null=True, upload_to='profiles/'),
        ),
    ]
