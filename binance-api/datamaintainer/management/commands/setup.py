from django.core.management.base import BaseCommand
from datamaintainer.models import KlineAllSymbol, Symbol
from config import Config
import datetime
import pytz
import multiprocessing

configs = Config()

print('''
            ░██████╗███████╗████████╗████████╗██╗███╗░░██╗░██████╗░  ██╗░░░██╗██████╗░░░░░░░░░░
            ██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗░██║██╔════╝░  ██║░░░██║██╔══██╗░░░░░░░░░
            ╚█████╗░█████╗░░░░░██║░░░░░░██║░░░██║██╔██╗██║██║░░██╗░  ██║░░░██║██████╔╝░░░░░░░░░
            ░╚═══██╗██╔══╝░░░░░██║░░░░░░██║░░░██║██║╚████║██║░░╚██╗  ██║░░░██║██╔═══╝░░░░░░░░░░
            ██████╔╝███████╗░░░██║░░░░░░██║░░░██║██║░╚███║╚██████╔╝  ╚██████╔╝██║░░░░░██╗██╗██╗
            ╚═════╝░╚══════╝░░░╚═╝░░░░░░╚═╝░░░╚═╝╚═╝░░╚══╝░╚═════╝░  ░╚═════╝░╚═╝░░░░░╚═╝╚═╝╚═╝
''')

def helper(sym):
        print(f"Got sym {sym}")
        interval = '1d'
        url = f"https://api.binance.us/api/v3/klines?symbol={sym}&interval={interval}"
        response = configs.session.get(url=url)
        local_tz = pytz.timezone('Asia/Kolkata')
        utc_tz = pytz.timezone('UTC')
        # print(f"Requested  with url {url}")
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
                close_date_time_localize = local_tz.localize(close_date_time)
                kline_all_symbol.close_date_time = close_date_time_localize.astimezone(utc_tz).replace(tzinfo=None)
                kline_all_symbol.symbol = sym
                if close_date_time.date() < datetime.datetime.now().date():
                    kline_all_symbol.save()
            return True
        else:
            # print(f" Status code : {response.status_code} Message  : {response.reason}")
            return False

class Command(BaseCommand):
    help = 'Runs startup code'

    def handle(self, *args, **options):
        try:
            response = configs.session.get(url='https://api.binance.com/api/v3/exchangeInfo')
            if response.status_code == 200:
                data = response.json()
                for symboleData in data['symbols']:
                    if symboleData['symbol'] != 'BTCUSD':
                        res = Symbol.objects.get_or_create(symbol=symboleData['symbol'])
                print("Symbol set up done...")
            else:
                print(f" Status code : {response.status_code} Message  : {response.reason}")
            symbol = list(Symbol.objects.all().exclude(symbol="BTCUSD").values_list("symbol", flat=True))
            helper('BTCUSD') # This required by all the symbols
            symbole_done = 0
            for sym in symbol:
                if helper(sym):
                    symbole_done += 1
                    if symbole_done > configs.symbols_to_hold:
                        break
        except Exception as e:
            print(f"Error in worker symbol : {e}")