from django.shortcuts import render
from django.http import FileResponse

from django.conf import settings

# Create your views here.


def home(request):
    return render(request, 'homepage/index.html')



def static(request, appname:str, filetype:str, filename:str):
    print("Served from function")
    return FileResponse(
        filename = settings.STATIC_ROOT / appname / filetype / filename
    )

def media(request, appname:str, filetype:str, filename:str):
    print("Served from function")
    return FileResponse(
        filename = settings.MEDIA_ROOT / appname / filetype / filename
    )
