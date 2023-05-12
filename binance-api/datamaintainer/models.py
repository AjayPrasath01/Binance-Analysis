from django.db import models
from django.utils import timezone
import datetime
from config import Config 

config = Config()

class ParanoidModel(models.Model):
    created_at = models.DateTimeField(null=True, default=None)
    updated_at = models.DateTimeField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        _datetime = datetime.datetime.now()
        if not self.created_at:
            self.created_at = _datetime
        self.updated_at = _datetime
        super().save(*args, **kwargs)

    def delete(self):
        self.deleted_at = datetime.datetime.now()
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
    open_date_time = models.DateTimeField(db_column='open_date_time', null=True, default=None)
    open = models.FloatField(db_column="open", null=True, default=None)
    high = models.FloatField(db_column="high", null=True, default=None)
    low = models.FloatField(db_column="low", null=True, default=None)
    close = models.FloatField(db_column="close", null=True, default=None)
    rsma = models.DecimalField(db_column="rsma", max_digits=32, decimal_places=14, null=True, default=None)
    rsma_200 = models.DecimalField(db_column="rsma_200", max_digits=32, decimal_places=14, null=True, default=None)
    volume = models.FloatField(db_column='volume', null=True, default=None)
    close_date_time = models.DateTimeField(db_column='close_date_time', null=True, default=None)
    symbol = models.CharField(db_column='symbol', max_length=200, null=True, default=None)
    rsd = models.FloatField(db_column="rsd", null=True, default=None)

    def save(self, *args, **kwargs):
        if not KlineAllSymbol.objects.filter(symbol=self.symbol, close_date_time=self.close_date_time).exists():
            _datetime = datetime.datetime.now()
            if not self.created_at:
                self.created_at = _datetime
            self.updated_at = _datetime
            if self.symbol != 'BTCUSD':
                try:
                    existing_instance = KlineAllSymbol.objects.get(symbol='BTCUSD', close_date_time=self.close_date_time)
                    self.rsma = float(self.close) / existing_instance.close
                    last_datetime = self.close_date_time
                    start_datetime = last_datetime - datetime.timedelta(days=config.moving_average - 1)
                    result = KlineAllSymbol.objects.filter(symbol=self.symbol, close_date_time__lte=last_datetime, close_date_time__gte=start_datetime)
                    if result.count() == (config.moving_average - 1):
                        self.rsma_200 = (float(result.aggregate(sum_value=models.Sum('rsma'))['sum_value']) + float(self.rsma)) / config.moving_average
                        self.rsd = ((self.rsma - float(self.rsma_200))/float(self.rsma_200)) * 100
                except Exception as e:
                    return
            super().save(*args, **kwargs)
    

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