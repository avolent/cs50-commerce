# Generated by Django 4.0.1 on 2022-01-31 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auctions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('starting_price', models.FloatField()),
                ('image', models.TextField()),
                ('category', models.CharField(max_length=64)),
                ('created', models.DateTimeField()),
            ],
        ),
    ]
