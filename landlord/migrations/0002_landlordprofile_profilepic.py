# Generated by Django 5.1.4 on 2025-01-08 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='landlordprofile',
            name='profilepic',
            field=models.ImageField(blank=True, null=True, upload_to='profiles/'),
        ),
    ]
