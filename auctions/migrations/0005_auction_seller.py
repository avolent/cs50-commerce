# Generated by Django 4.0.1 on 2022-01-31 01:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_auction_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='seller',
            field=models.ManyToManyField(blank=True, related_name='seller', to=settings.AUTH_USER_MODEL),
        ),
    ]