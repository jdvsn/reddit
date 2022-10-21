# Generated by Django 4.1 on 2022-10-21 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0022_alter_post_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='subreddit',
            name='moderators',
            field=models.ManyToManyField(related_name='subreddits_moderated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subreddit',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subreddits_created', to=settings.AUTH_USER_MODEL),
        ),
    ]
