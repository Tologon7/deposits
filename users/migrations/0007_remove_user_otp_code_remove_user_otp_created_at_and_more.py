# Generated by Django 5.1.2 on 2024-11-21 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_otp_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='otp_code',
        ),
        migrations.RemoveField(
            model_name='user',
            name='otp_created_at',
        ),
        migrations.DeleteModel(
            name='OTP',
        ),
    ]
