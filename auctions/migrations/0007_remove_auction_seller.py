# Generated by Django 4.0.1 on 2022-01-31 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_auction_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='seller',
        ),
    ]
