# Generated by Django 2.2.19 on 2021-04-17 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
