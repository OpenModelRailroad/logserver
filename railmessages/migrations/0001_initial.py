# Generated by Django 3.0.7 on 2020-12-25 12:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sniffer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_type', models.CharField(max_length=50)),
                ('msg_json', models.CharField(max_length=512)),
                ('msg_raw', models.CharField(max_length=50, null=True)),
                ('recv_date', models.DateField(auto_now=True)),
                ('recv_time', models.TimeField(auto_now=True)),
                ('sniffer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='sniffer.Sniffer')),
            ],
        ),
        migrations.CreateModel(
            name='CommandMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.IntegerField()),
                ('sniffer', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.PROTECT, to='sniffer.Sniffer')),
            ],
        ),
        migrations.AddIndex(
            model_name='rawmessage',
            index=models.Index(fields=['id', 'msg_raw'], name='railmessage_id_4836a3_idx'),
        ),
        migrations.AddIndex(
            model_name='commandmessage',
            index=models.Index(fields=['id', 'address', 'sniffer'], name='railmessage_id_e54dcf_idx'),
        ),
    ]
