# Generated by Django 3.0.6 on 2020-09-16 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appsettings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appsettings',
            name='value',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]