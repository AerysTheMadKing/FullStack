# Generated by Django 4.2 on 2023-04-13 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='forgot_password_reset',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]