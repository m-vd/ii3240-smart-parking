# Generated by Django 2.1.7 on 2019-04-29 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20190428_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='userType',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
