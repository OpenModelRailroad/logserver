# Generated by Django 3.0.7 on 2021-01-08 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0002_clients_verbose_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='verbose_name',
            field=models.CharField(max_length=512, unique=True),
        ),
    ]
