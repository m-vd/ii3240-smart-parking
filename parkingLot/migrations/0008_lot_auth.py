# Generated by Django 2.0.7 on 2019-05-15 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkingLot', '0007_auto_20190504_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='auth',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]