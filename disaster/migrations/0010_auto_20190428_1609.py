# Generated by Django 2.0.7 on 2019-04-28 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disaster', '0009_auto_20190428_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disaster',
            name='location',
            field=models.ManyToManyField(blank=True, to='parkingLot.Lot'),
        ),
    ]