from django.core.management.base import BaseCommand
from datamaintainer.models import KlineAllSymbol, Symbol
from config import Config
import datetime
import pytz
from django_q.models import Schedule
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
      
def printOk():
        print('\033[92mOK \033[0m')

def printStatusCode(code, message=""):
    print(f"\033[91m {code} {message} \033[0m", end=" ")

def printFailed():
    print('\033[91mFailed \033[0m')

def helper(sym):
        print(f"Getting Data of symbol {sym}", end="....")
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
            printOk()
            return True
        else:
            printStatusCode(response.status_code, response.reason)
            printFailed()
            return False

class Command(BaseCommand):
    help = 'Runs startup code'

    def handle(self, *args, **options):
        try:
            #  pass
            print("Symbol set up done...", end="...")
            response = configs.session.get(url='https://api.binance.com/api/v3/exchangeInfo')
            if response.status_code == 200:
                data = response.json()
                for symboleData in data['symbols']:
                    if symboleData['symbol'] != 'BTCUSD':
                        res = Symbol.objects.get_or_create(symbol=symboleData['symbol'])
                printOk()
            else:
                printStatusCode(response.status_code, response.reason)
                printFailed()
            symbol = list(Symbol.objects.all().exclude(symbol="BTCUSD").values_list("symbol", flat=True))
            if KlineAllSymbol.objects.exists():
                print('''\033[91m
                ___________      .__.__             .___
                \_   _____/____  |__|  |   ____   __| _/
                |    __) \__  \ |  |  | _/ __ \ / __ | 
                |     \   / __ \|  |  |_\  ___// /_/ | 
                \___  /  (____  /__|____/\___  >____ | 
                    \/        \/             \/     \/ 
                \033[0m''')
                print('\033[91mkline_all_symbol Table must be truncated before setup. \033[0m')
                exit(2)
            helper('BTCUSD') # This required by all the symbols
            helper('ADAUSD')
            symbole_done = 0
            for sym in symbol:
                if helper(sym):
                    symbole_done += 1
                    if symbole_done > configs.symbols_to_hold:
                        break
        except Exception as e:
            printStatusCode(0, e)
            printFailed()
        finally:
            Schedule.objects.all().delete()
            current_datetime = datetime.datetime.now()
            next_run_time = current_datetime
            if current_datetime.time() > datetime.time(5, 30):
                next_run_time = (datetime.datetime.now() + datetime.timedelta(days=1)).replace(minute=31, hour=5)
            else:
                next_run_time = datetime.datetime.now() 
            next_run_time = next_run_time.replace(minute=31, hour=5)
            Schedule.objects.create(func="datamaintainer.tasks.data_updater", name="Data Adder", schedule_type=Schedule.DAILY, next_run=next_run_time)
            
            