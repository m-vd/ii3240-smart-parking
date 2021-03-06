# Generated by Django 2.1.7 on 2019-04-15 18:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticketID', models.UUIDField(default=uuid.UUID('20396198-a1c6-4d07-910c-a21bed1d4d02'), editable=False, primary_key=True, serialize=False)),
                ('entryTime', models.DateTimeField(auto_now_add=True)),
                ('exitTime', models.DateTimeField(null=True)),
            ],
        ),
    ]
