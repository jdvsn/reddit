# Generated by Django 4.1 on 2022-10-21 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0023_subreddit_moderators_alter_subreddit_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='subreddit',
            name='subreddit_info',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]
