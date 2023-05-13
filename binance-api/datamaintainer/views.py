from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from config import Config
from django.utils import timezone
from . import models
import json
from django_q.tasks import async_task, result
from django_q.models import Task
from django.db.models import Max
from django.contrib.auth.decorators import login_required

# Create your views here.

configs = Config()


def fetch_data(request):
    # if request.method == 'PUT':
    #     symbol = request.GET.get('symbol')
    #     isAll = request.GET.get("all")
    #     if not symbol and not isAll:
    #         return JsonResponse({"message": "Symbol param is missing"}, status=400)
    #     task = async_task("datamaintainer.tasks.data_updater", symbol, isAll)
    #     result(task)
    #     return JsonResponse({"message": "Done"})
    # else:
     return JsonResponse({"message": "Not implemented at production"}, status=501)
    
def update_symbol_list(request):
    if request.method == 'PUT':
        # task = async_task("datamaintainer.tasks.symbol_updater")
        # print(result(task))
        return JsonResponse({"message": "Not implemented at production"}, status=501)
    else:
        return JsonResponse({"message": "Only PUT is allowed at the end point"}, status=405)
    
def fetch_all_available_data(request):
    if (request.user.is_authenticated):
        if request.method == 'GET':
            latest_close_time = models.KlineAllSymbol.objects.aggregate(Max('close_date_time'))['close_date_time__max']
            latest_data = models.KlineAllSymbol.objects.filter(close_date_time=latest_close_time)
            latest_data = latest_data.values_list("close_date_time", "rsma", "rsma_200", "rsd", "symbol") 
            key_value_pairs = [
            {"close_date_time": row[0], "rsma": row[1], "rsma_200": row[2], "rsd": row[3], "symbol": row[4]}
            for row in latest_data
            ]
            return JsonResponse({"data": key_value_pairs})
        return JsonResponse({"message": "Method not allowed"}, status=405)
    return JsonResponse({"message": "Unauthorized"}, status=401)
