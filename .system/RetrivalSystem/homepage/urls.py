# -*- coding: utf-8 -*-
"""
Created on Sun May 28 13:55:48 2023

@author: admin
"""

from django.urls import path
from .views import (
    home, 
)

urlpatterns = [
    path('', home, name='homepage-home'), 
    
]
