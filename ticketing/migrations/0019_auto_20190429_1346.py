# Generated by Django 2.1.7 on 2019-04-29 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0018_auto_20190429_1315'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='userID',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parkingLot.Lot'),
        ),
    ]
