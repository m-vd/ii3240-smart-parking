# Generated by Django 2.1.7 on 2019-04-24 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0003_auto_20190424_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='location',
            field=models.CharField(default='', editable=False, max_length=30),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='userID',
            field=models.CharField(editable=False, max_length=30),
        ),
    ]
