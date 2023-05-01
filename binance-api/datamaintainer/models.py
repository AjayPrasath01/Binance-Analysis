from django.db import models
from django.utils import timezone
import datetime

class ParanoidModel(models.Model):
    created_at = models.DateTimeField(null=True, default=None)
    updated_at = models.DateTimeField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        aware_datetime = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
        if not self.created_at:
            self.created_at = aware_datetime
        self.updated_at = aware_datetime
        super().save(*args, **kwargs)

    def delete(self):
        aware_datetime = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
        self.deleted_at = aware_datetime
        self.save()

    def undelete(self):
        self.deleted_at = None
        self.save()


class ParanoidManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)



class KlineAllSymbol(ParanoidModel):
    class Meta:
        db_table = "kline_all_symbol"

    objects = ParanoidManager()

    kline_all_id = models.AutoField(db_column="kline_all_id", null=False, primary_key=True)
    open_time = models.CharField(db_column='open_time', max_length=200, null=True, default=None)
    open_date_time = models.DateTimeField(db_column='open_date_time', null=True, default=None)
    open = models.IntegerField(db_column="open", null=True, default=None)
    high = models.IntegerField(db_column="high", null=True, default=None)
    low = models.IntegerField(db_column="low", null=True, default=None)
    close = models.FloatField(db_column="close", null=True, default=None)
    rsma = models.DecimalField(db_column="rsma", max_digits=10, decimal_places=8, null=True, default=None)
    close_date = models.DateField(db_column="close_date", null=True, default=None)
    volume = models.IntegerField(db_column='volume', null=True, default=None)
    close_time = models.CharField(db_column='close_time', max_length=200, null=True, default=None)
    close_date_time = models.DateTimeField(db_column='close_date_time', null=True, default=None)
    quote_asset_volume = models.IntegerField(db_column="quote_asset_volume", null=True, default=None)
    number_of_trades = models.IntegerField(db_column="number_of_trades", null=True, default=None)
    taker_buy_base_asset_volume = models.IntegerField(db_column="taker_buy_base_asset_volume", null=True, default=None)
    taker_buy_quote_asset_volume = models.IntegerField(db_column="taker_buy_quote_asset_volume", null=True, default=None)
    ignore = models.IntegerField(db_column="ignore", null=True, default=None)
    symbol = models.CharField(db_column='symbol', max_length=200, null=True, default=None)
    

class User(ParanoidModel):
    class Meta:
        db_table = "user"

    objects = ParanoidManager()

    user_id = models.AutoField(db_column='user_id', primary_key=True)
    username = models.CharField(db_column='username', max_length=100)
    password = models.CharField(db_column='password', max_length=150)
    name = models.CharField(db_column='name', max_length=200)
    status = models.IntegerField(db_column='status', default=1)
    login_count = models.IntegerField(db_column='login_count', default=0)


class Symbol(ParanoidModel):
    class Meta:
        db_table = 'symbols'

    objects = ParanoidManager()

    id  = models.AutoField(db_column='id', primary_key=True)
    symbol = models.CharField(db_column='symbol', max_length=200)
    price = models.IntegerField(db_column='price')
    priority = models.IntegerField(default=1, db_column='priority')