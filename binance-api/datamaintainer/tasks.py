from datamaintainer.models import KlineAllSymbol, Symbol
from config import Config
import datetime
import pytz
from django_q.tasks import async_task, schedule

configs = Config()

def data_updater(symbol=None, isAll=False):
    if symbol is None:
        symbol = list(KlineAllSymbol.objects.values_list('symbol', flat=True).distinct())
    else:
        symbol = [symbol]
    if isAll:
        symbol = Symbol.objects.all().values_list("symbol", flat=True)
    interval = '1d'
    for sym in symbol:
        url = None
        daysDifferent = 1 # To make intial request
        if KlineAllSymbol.objects.filter(symbol=sym).exists():
            kline_all_symbol = KlineAllSymbol.objects.filter(symbol=sym).latest('updated_at')
            print(kline_all_symbol)

            startDate  = kline_all_symbol.close_date_time
            starteDateTimeStamp = int(startDate.timestamp() * 1000)

            endDate = datetime.datetime.utcnow()
            check_time = datetime.datetime(endDate.year, endDate.month, endDate.day, 5, 29)

            if endDate.time() < check_time.time():
                endDate -= datetime.timedelta(days=1)

            endDate = endDate + datetime.timedelta(days=1)
            endDateTimesatmp =  int(endDate.timestamp() * 1000)
            print(f'endDateTimesatmp {endDateTimesatmp}')

            startDateTemp = int(startDate.replace(minute=28, second=0).timestamp() * 1000)
            deltaDate =  datetime.datetime.fromtimestamp(endDateTimesatmp/1000) - datetime.datetime.fromtimestamp(startDateTemp/1000)
            if deltaDate.days >= 1:
                url = f"https://api.binance.us/api/v3/klines?symbol={sym}&interval={interval}&startTime={starteDateTimeStamp}&endTime={endDateTimesatmp}"
                print(f"https://api.binance.us/api/v3/klines?symbol={sym}&interval={interval}&startTime={datetime.datetime.fromtimestamp(starteDateTimeStamp/1000)}&endTime={datetime.datetime.fromtimestamp(endDateTimesatmp/1000) }")
            daysDifferent = deltaDate.days
            print(deltaDate.days)
            print(f"Sym = {sym} Start datetime : {startDate} end datetime : {endDate}")


        if daysDifferent > 0:
            if url is None:
                url = f"https://api.binance.us/api/v3/klines?symbol={sym}&interval={interval}"
            response = configs.session.get(url=url)
            local_tz = pytz.timezone('Asia/Kolkata')
            utc_tz = pytz.timezone('UTC')
            print(f"Requested  with url {url}")
            if response.status_code == 200: 
                datum = response.json()
                for data in datum:
                    kline_all_symbol = KlineAllSymbol()
                    open_date_time = datetime.datetime.fromtimestamp(data[0]/1000)
                    open_date_time_localize = local_tz.localize(open_date_time)
                    kline_all_symbol.open_date_time = open_date_time_localize.astimezone(utc_tz).replace(tzinfo=None)
                    kline_all_symbol.open = data[1]
                    kline_all_symbol.high = data[2]
                    kline_all_symbol.low = data[3]
                    kline_all_symbol.close = data[4]
                    kline_all_symbol.volume = data[5]

                    close_date_time = datetime.datetime.fromtimestamp(data[6]/1000)
                    print(f"Close date time got {close_date_time} condition {close_date_time.date() < datetime.datetime.now().date()}")
                    close_date_time_localize = local_tz.localize(close_date_time)
                    kline_all_symbol.close_date_time = close_date_time_localize.astimezone(utc_tz).replace(tzinfo=None)
                    kline_all_symbol.symbol = sym
                    if close_date_time < datetime.datetime.now().replace(hour=5, minute=30):
                        kline_all_symbol.save()
            else:
                print(f" Status code : {response.status_code} Message  : {response.reason}")

def symbol_updater():
    try:
        response = configs.session.get(url='https://api.binance.com/api/v3/exchangeInfo')
        if response.status_code == 200:
            data = response.json()
            for symboleData in data['symbols']:
                if symboleData['symbol'] != 'BTCUSD':
                    Symbol.objects.get_or_create(symbol=symboleData['symbol'])
        else:
            print(f" Status code : {response.status_code} Message  : {response.reason}")
    except Exception as e:
        print(f"Error in worker symbol : {e}")