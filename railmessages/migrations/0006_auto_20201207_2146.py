# Generated by Django 3.0.6 on 2020-12-07 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railmessages', '0005_auto_20201207_2144'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='commandmessage',
            index=models.Index(fields=['id', 'address'], name='railmessage_id_b87e04_idx'),
        ),
    ]
