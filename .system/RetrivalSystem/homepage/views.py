from django.shortcuts import render
from django.http import FileResponse

from django.conf import settings

# Create your views here.


def home(request):
    return render(request, 'homepage/index.html')

def static(request, filename:str):
    return FileResponse(
        settings.STATIC_ROOT / filename
    )

def media(request, filename:str):
    return FileResponse(
        settings.MEDIA_ROOT / filename
    )