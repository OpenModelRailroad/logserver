# Generated by Django 3.0.7 on 2020-12-25 12:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sniffer', '0001_initial'),
        ('railmessages', '0003_auto_20201225_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commandmessage',
            name='sniffer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sniffer.Sniffer'),
        ),
    ]