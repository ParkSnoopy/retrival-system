from django.shortcuts import render
from django.http import FileResponse

from django.conf import settings

# Create your views here.


def home(request):
    return render(request, 'homepage/index.html')



def static(request, appname:str, filetype:str, filename:str):
    return FileResponse(
        open( settings.STATIC_ROOT / appname / filetype / filename , 'rb' )
    )

def media(request, appname:str, filetype:str, filename:str):
    return FileResponse(
        open( settings.MEDIA_ROOT / appname / filetype / filename , 'rb' )
    )
