# Generated by Django 3.0.6 on 2020-11-30 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sniffer', '0004_auto_20200917_0046'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_type', models.CharField(max_length=50)),
                ('msg_json', models.CharField(max_length=512)),
                ('msg_raw', models.CharField(max_length=50, null=True)),
                ('insert_date', models.DateField(auto_now=True)),
                ('sniffer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='sniffer.Sniffer')),
            ],
        ),
    ]