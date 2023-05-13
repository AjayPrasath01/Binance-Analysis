from django.shortcuts import render
from django.http import HttpResponse, FileResponse, HttpResponseNotFound, JsonResponse
import os, json
from django.contrib.auth.forms import AuthenticationForm
from pathlib import Path
from django.views.static import serve
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'index.html')

def file_handler(request, path):
    path = 'static/' + path
    BASE_DIR = Path(__file__).resolve().parent.parent
    print(os.path.join(BASE_DIR, path))
    file_path = os.path.join(BASE_DIR, path)
    return serve(request, 'favicon.ico', document_root=path)

def login_view(request):
    if request.method == 'POST':
        print(f"Request body {request.body}")
        if len(request.body) == 0:
            return JsonResponse({"message": "Wrong credentials"}, status=401)
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        username = body_data.get('username')
        password = body_data.get('password')
        print(username , password)
        if username != None and password != None:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Logged in'})
            else:
                return JsonResponse({"message": "Wrong credentials"}, status=401)
    else:
        return JsonResponse({"message": "Only post allowed"}, status=405)
    
    return JsonResponse({"message": "Wrong redentials"}, status=401)

def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Loged out"})