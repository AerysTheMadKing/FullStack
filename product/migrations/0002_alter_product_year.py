# Generated by Django 4.2 on 2023-04-15 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='year',
            field=models.DateField(),
        ),
    ]