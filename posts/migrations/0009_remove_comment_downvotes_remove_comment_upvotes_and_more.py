# Generated by Django 4.1 on 2022-09-16 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_comment_created_by_post_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='downvotes',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='upvotes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='downvotes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='upvotes',
        ),
    ]
