# Generated by Django 3.0.7 on 2021-01-09 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railmessages', '0010_auto_20210107_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandmessage',
            name='console',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]