# Generated by Django 3.2 on 2021-04-21 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ConferenceRoom', '0005_reservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='date',
            field=models.DateField(),
        ),
    ]
