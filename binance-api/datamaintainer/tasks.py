from datamaintainer.models import KlineAllSymbol
from config import Config
from django.utils import timezone
import datetime

configs = Config()

def _time_zone_datetime(timestamp, time_zone=None):
    if time_zone:
        return timezone.make_aware(datetime.datetime.fromtimestamp(timestamp/1000), time_zone) 
    return timezone.make_aware(datetime.datetime.fromtimestamp(timestamp/1000), timezone.get_default_timezone()) 

def data_updater(symbol=None):
    if symbol is None:
        symbol = KlineAllSymbol.objects.values_list('symbol', flat=True).distinct()
    symbol = [symbol]
    interval = '1d'
    for sym in symbol:
        url = None
        daysDifferent = 1 # To make intial request
        if KlineAllSymbol.objects.filter(symbol=sym).exists():
            kline_all_symbol = KlineAllSymbol.objects.filter(symbol=sym).latest('updated_at')
            startDate  = kline_all_symbol.close_date
            starteDateTimeStamp = int(datetime.datetime.combine(startDate, datetime.time.min).timestamp() * 1000)
            endDate = datetime.datetime.now().date()
            endDateTimesatmp =  int(datetime.datetime.combine(endDate, datetime.time.min).timestamp() * 1000)
            deltaDate =  endDate - startDate
            if deltaDate.days >= 1:
                url = f"https://api.binance.us/api/v3/klines?symbol={sym}&interval={interval}&startTime={starteDateTimeStamp}&endTime={endDateTimesatmp}"
            daysDifferent = deltaDate.days
            print(deltaDate.days)
            print(f"Sym = {sym} Start datetime : {starteDateTimeStamp} end datetime : {endDateTimesatmp}")

        if daysDifferent > 0:
            if url is None:
                url = f"https://api.binance.us/api/v3/klines?symbol={sym}&interval={interval}"
            response = configs.session.get(url=url)
            print(f"Requested  with url {url}")
            if response.status_code == 200: 
                datum = response.json()
                for data in datum:
                    kline_all_symbol = KlineAllSymbol()
                    kline_all_symbol.open_time = datetime.datetime.utcfromtimestamp(data[0]/1000)
                    kline_all_symbol.open_date_time = _time_zone_datetime(data[0])
                    kline_all_symbol.open = int(float(data[1]))
                    kline_all_symbol.high = int(float(data[2]))
                    kline_all_symbol.low = int(float(data[3]))
                    kline_all_symbol.close = data[4]
                    kline_all_symbol.volume = int(float(data[5]))

                    date_time = _time_zone_datetime(data[6])
                    kline_all_symbol.close_date_time = date_time
                    kline_all_symbol.close_time = date_time
                    kline_all_symbol.close_date = date_time.date()

                    kline_all_symbol.quote_asset_volume = int(float(data[7]))
                    kline_all_symbol.number_of_trades = data[8]
                    kline_all_symbol.taker_buy_base_asset_volume = int(float(data[9]))
                    kline_all_symbol.taker_buy_quote_asset_volume = int(float(data[10]))
                    kline_all_symbol.ignore = data[11]
                    kline_all_symbol.symbol = sym
                    kline_all_symbol.save()
            else:
                print(f" Status code : {response.status_code} Message  : {response.reason}")