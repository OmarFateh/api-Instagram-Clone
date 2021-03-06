# Generated by Django 2.2.19 on 2021-04-14 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('item', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(blank=True, choices=[('sent', 'sent'), ('accepted', 'accepted')], max_length=8, null=True)),
                ('notification_type', models.CharField(choices=[('like', 'like'), ('comment', 'comment'), ('follow', 'follow'), ('tag', 'tag'), ('follow_request', 'follow request'), ('comment_like', 'comment like')], max_length=14)),
                ('comment_snippt', models.CharField(blank=True, max_length=90, null=True)),
                ('is_seen', models.BooleanField(default=False)),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_comment', to='item.Comment')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_item', to='item.Item')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='noti_to_user', to='profiles.UserProfile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='noti_from_user', to='profiles.UserProfile')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'ordering': ['-created_at'],
            },
        ),
    ]
