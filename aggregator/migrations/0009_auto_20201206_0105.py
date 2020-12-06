# Generated by Django 3.1.1 on 2020-12-06 01:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aggregator', '0008_auto_20201029_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursefield',
            name='private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='coursefield',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
