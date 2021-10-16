from django.contrib import admin
from django.urls import path , include
from .views import *

urlpatterns = [
    path('<int:T>/<int:H>', savedata ),
    path('getdata', getdata ),
    path('getpidtdata', getpidtdata ),
    path('getpidhdata', getpidhdata ),
    path('testcase', testcase ),

    path('',index , name='index'),
    path('automode', automode , name='automode'),
    path('manualmode',manualmode , name='manualmode'),
    
]
