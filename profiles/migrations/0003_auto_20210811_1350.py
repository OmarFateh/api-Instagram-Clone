# Generated by Django 2.2.19 on 2021-08-11 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_followrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followrequest',
            name='status',
            field=models.CharField(blank=True, choices=[('sent', 'sent'), ('accepted', 'accepted'), ('declined', 'declined')], max_length=8, null=True),
        ),
    ]