# Generated by Django 2.1.7 on 2019-04-29 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disaster', '0014_auto_20190429_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disaster',
            name='location',
            field=models.ManyToManyField(blank=True, to='parkingLot.Lot'),
        ),
    ]