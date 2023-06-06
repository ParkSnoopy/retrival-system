# -*- coding: utf-8 -*-
"""
Created on Sun May 28 13:55:48 2023

@author: admin
"""

from django.urls import path
from django.shortcuts import redirect

from .views import (
    home, 
    login_view, 
    logout_view, 
    static, 
    media, 
)


urlpatterns = [
    path('', lambda request: redirect('homepage-home', status='0')), 
    path('<str:status>', home, name='homepage-home'), 
    
    path('login/', login_view, name='login'), 
    path('logout/', logout_view, name='logout'), 
    
    path('static/<str:appname>/<str:filetype>/<str:filename>', static), 
    path('media/<str:appname>/<str:filetype>/<str:filename>', media), 
]
