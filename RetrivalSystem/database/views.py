from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

from .db_control import read_and_create_from

# Create your views here.


@user_passes_test( lambda user: user.is_superuser )
def create(request):
    
    response = redirect('homepage-home')
    
    try:
        read_and_create_from("data.csv")
        response.set_cookie('db_create', '0')
    except Exception as exc:
        print(f"\n  While building DB : {exc}\n\n")
        response.set_cookie('db_create', '1')
    
    return response