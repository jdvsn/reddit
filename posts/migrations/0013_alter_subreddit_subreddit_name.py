# Generated by Django 4.1 on 2022-09-20 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_alter_post_post_body_alter_post_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subreddit',
            name='subreddit_name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
