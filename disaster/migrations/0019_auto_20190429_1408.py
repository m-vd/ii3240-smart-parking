# Generated by Django 2.1.7 on 2019-04-29 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parkingLot', '0006_auto_20190429_1349'),
        ('disaster', '0018_auto_20190429_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disaster',
            name='location',
        ),
        migrations.AddField(
            model_name='disaster',
            name='location',
            field=models.ForeignKey(default='a', on_delete=django.db.models.deletion.CASCADE, to='parkingLot.Lot'),
            preserve_default=False,
        ),
    ]
