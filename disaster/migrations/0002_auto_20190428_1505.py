# Generated by Django 2.0.7 on 2019-04-28 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disaster', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disaster',
            name='location',
            field=models.ManyToManyField(blank=True, to='parkingLot.Lot'),
        ),
    ]
