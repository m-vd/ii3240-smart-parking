# Generated by Django 2.0.7 on 2019-04-28 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20190424_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userEmail',
            field=models.EmailField(max_length=50),
        ),
    ]