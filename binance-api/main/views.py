from django.shortcuts import render
from django.http import HttpResponse, FileResponse, HttpResponseNotFound
import os
from pathlib import Path
from django.views.static import serve
from django.conf import settings

def index(request):
    return render(request, 'index.html')

def file_handler(request, path):
    path = 'static/' + path
    BASE_DIR = Path(__file__).resolve().parent.parent
    print(os.path.join(BASE_DIR, path))
    file_path = os.path.join(BASE_DIR, path)
    return serve(request, 'favicon.ico', document_root=path)