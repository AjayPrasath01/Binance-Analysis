# Generated by Django 3.2.18 on 2023-05-03 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamaintainer', '0004_auto_20230430_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='klineallsymbol',
            name='close_date',
        ),
        migrations.RemoveField(
            model_name='klineallsymbol',
            name='close_time',
        ),
        migrations.RemoveField(
            model_name='klineallsymbol',
            name='ignore',
        ),
        migrations.RemoveField(
            model_name='klineallsymbol',
            name='number_of_trades',
        ),
        migrations.RemoveField(
            model_name='klineallsymbol',
            name='open_time',
        ),
        migrations.RemoveField(
            model_name='klineallsymbol',
            name='quote_asset_volume',
        ),
        migrations.RemoveField(
            model_name='klineallsymbol',
            name='taker_buy_base_asset_volume',
        ),
        migrations.RemoveField(
            model_name='klineallsymbol',
            name='taker_buy_quote_asset_volume',
        ),
        migrations.AlterField(
            model_name='klineallsymbol',
            name='high',
            field=models.FloatField(db_column='high', default=None, null=True),
        ),
        migrations.AlterField(
            model_name='klineallsymbol',
            name='low',
            field=models.FloatField(db_column='low', default=None, null=True),
        ),
        migrations.AlterField(
            model_name='klineallsymbol',
            name='open',
            field=models.FloatField(db_column='open', default=None, null=True),
        ),
        migrations.AlterField(
            model_name='klineallsymbol',
            name='volume',
            field=models.FloatField(db_column='volume', default=None, null=True),
        ),
    ]
