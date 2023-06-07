# -*- coding: utf-8 -*-
"""
Created on Sun May 28 13:52:55 2023

@author: admin
"""

from django.urls import path
from .views import (
    home, 
    details, 
)
from .view_tmp import (
    home_yly, 
)

urlpatterns = [
    path('', home, name='search-home'), 
    path('details/<int:article_pk>', details), 
    
    path('yly/', home_yly), 
]
