# Generated by Django 4.1 on 2022-10-27 12:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tier', models.CharField(choices=[('gold', 'gold'), ('silver', 'silver'), ('bronze', 'bronze')], max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('purchased_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchased_awards', to=settings.AUTH_USER_MODEL)),
                ('sent_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_awards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
