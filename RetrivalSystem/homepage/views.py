from django.shortcuts import render, redirect
from django.http import FileResponse

from django.contrib.auth import authenticate, login, logout
from django.conf import settings

# Create your views here.


def home(request):
    
    status = 0
    if request.method == "POST":
        # print(f"\n  {request.POST = }\n")
        searchinput = request.POST.get('searchinput')
        if searchinput:
            return redirect('search-home', searchinput=searchinput)
        status = 1
    
    db_create_status = request.COOKIES.get('db_create', None)
    response = render(request, 'homepage/index.html', {
        'status': status, 
        'db_create_status': db_create_status, 
    })
    
    if db_create_status:
        response.delete_cookie('db_create')
    
    return response



def login_view(request):
    status = 0
    if request.method == "POST":
        username = request.POST.get('id')
        password = request.POST.get('pw')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('homepage-home')
        status = 1
    return render(request, 'accounts/login.html', {'status': status})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('homepage-home')


def static(request, appname:str, filetype:str, filename:str):
    return FileResponse(
        open( settings.STATIC_ROOT / appname / filetype / filename , 'rb' )
    )

def media(request, appname:str, filetype:str, filename:str):
    return FileResponse(
        open( settings.MEDIA_ROOT / appname / filetype / filename , 'rb' )
    )
