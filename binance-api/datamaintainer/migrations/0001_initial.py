# Generated by Django 3.2.18 on 2023-05-04 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KlineAllSymbol',
            fields=[
                ('created_at', models.DateTimeField(default=None, null=True)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('kline_all_id', models.AutoField(db_column='kline_all_id', primary_key=True, serialize=False)),
                ('open_date_time', models.DateTimeField(db_column='open_date_time', default=None, null=True)),
                ('open', models.FloatField(db_column='open', default=None, null=True)),
                ('high', models.FloatField(db_column='high', default=None, null=True)),
                ('low', models.FloatField(db_column='low', default=None, null=True)),
                ('close', models.FloatField(db_column='close', default=None, null=True)),
                ('rsma', models.DecimalField(db_column='rsma', decimal_places=8, default=None, max_digits=10, null=True)),
                ('rsma_200', models.DecimalField(db_column='rsma_200', decimal_places=8, default=None, max_digits=10, null=True)),
                ('volume', models.FloatField(db_column='volume', default=None, null=True)),
                ('close_date_time', models.DateTimeField(db_column='close_date_time', default=None, null=True)),
                ('symbol', models.CharField(db_column='symbol', default=None, max_length=200, null=True)),
                ('rsd', models.FloatField(db_column='rsd', default=None, null=True)),
            ],
            options={
                'db_table': 'kline_all_symbol',
            },
        ),
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('created_at', models.DateTimeField(default=None, null=True)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('symbol', models.CharField(db_column='symbol', max_length=200)),
            ],
            options={
                'db_table': 'symbols',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('created_at', models.DateTimeField(default=None, null=True)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('user_id', models.AutoField(db_column='user_id', primary_key=True, serialize=False)),
                ('username', models.CharField(db_column='username', max_length=100)),
                ('password', models.CharField(db_column='password', max_length=150)),
                ('name', models.CharField(db_column='name', max_length=200)),
                ('status', models.IntegerField(db_column='status', default=1)),
                ('login_count', models.IntegerField(db_column='login_count', default=0)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
