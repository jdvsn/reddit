# Generated by Django 4.1 on 2022-10-27 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_alter_award_purchased_by'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Award',
        ),
    ]
