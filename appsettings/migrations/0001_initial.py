# Generated by Django 3.0.6 on 2020-11-23 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appsettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'verbose_name': 'Settings',
                'verbose_name_plural': 'Settings',
            },
        ),
    ]
