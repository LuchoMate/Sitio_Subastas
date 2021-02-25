# Generated by Django 3.1.5 on 2021-02-03 00:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20210201_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='author',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='auction_listing',
            name='img_url',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='bids',
            name='id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='listing_bid', serialize=False, to='auctions.auction_listing'),
        ),
        migrations.AlterField(
            model_name='user',
            name='member_since',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_watchlist', to='auctions.auction_listing')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_watchlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_author', models.CharField(max_length=150)),
                ('commentary_date', models.DateTimeField(auto_now_add=True)),
                ('listing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_comment', to='auctions.auction_listing')),
            ],
        ),
        migrations.AddConstraint(
            model_name='watchlist',
            constraint=models.UniqueConstraint(fields=('listing_id', 'user_id'), name='unique_watchlist'),
        ),
    ]