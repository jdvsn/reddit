# Generated by Django 4.1 on 2022-09-12 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_comment_reply'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CommentReply',
        ),
    ]
