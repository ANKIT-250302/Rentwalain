# Generated by Django 5.1.4 on 2025-01-08 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0002_tenantprofile_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenantprofile',
            name='profilepic',
            field=models.ImageField(blank=True, default='profiles/unnamed.webp', null=True, upload_to='profiles/'),
        ),
    ]