# Generated by Django 4.1 on 2022-11-10 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0027_post_post_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_type',
        ),
    ]
