from django.contrib import admin
from django.urls import path , include
from .views import *

urlpatterns = [
    path('<int:H>/<int:T>', savedata ),
    path('getdata', getdata ),

    path('',index , name='index'),
    path('automode', automode , name='automode'),
    path('manualmode',manualmode , name='manualmode'),
    
]
