from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

from .reader import read_and_create_from

# Create your views here.


@user_passes_test( lambda user: user.is_superuser )
def create(request):
    
    response = redirect('homepage-home')
    
    try:
        read_and_create_from("jilin_in_data3.csv")
        response.set_cookie('db_create', '0')
    except:
        response.set_cookie('db_create', '1')
    
    return response