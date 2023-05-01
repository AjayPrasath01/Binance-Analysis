from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from config import Config
from django.utils import timezone
import datetime
from django_q.tasks import async_task, result
from django_q.models import Task

Task.objects.all().delete()

# Create your views here.

configs = Config()


def fetch_data(request):
    if request.method == 'GET':
        symbol = request.GET.get('symbol')
        if not symbol:
            return JsonResponse({"message": "Symbol param is missing"}, status=400)
        interval = '1d'
        task = async_task("datamaintainer.tasks.data_updater", symbol)
        result(task)
        return JsonResponse({"message": "Done"})
    else:
        return JsonResponse({"message": "Only GET is allowed at the end point"}, status=405)
