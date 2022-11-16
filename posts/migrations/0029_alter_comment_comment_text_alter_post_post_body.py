# Generated by Django 4.1 on 2022-11-10 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0028_remove_post_post_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_text',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_body',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]