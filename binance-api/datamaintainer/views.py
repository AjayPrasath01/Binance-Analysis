from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from config import Config
from django.utils import timezone
from . import models
import json
from django_q.tasks import async_task, result
from django_q.models import Task
from django.db.models import F, Max, Q

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
    if request.method == 'GET':
        latest_close_time = models.KlineAllSymbol.objects.aggregate(Max('close_date_time'))['close_date_time__max']
        latest_data = models.KlineAllSymbol.objects.filter(close_date_time=latest_close_time).values('symbol', 'rsd')
    return JsonResponse(dict(latest_data.values_list('symbol', 'rsd')))
