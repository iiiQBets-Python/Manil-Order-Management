from django.urls import path
from .views import *

urlpatterns = [   
    
    path('C_order_table', C_order_table, name='C_order_table'),
    path('C_dispatch_details', C_dispatch_details, name='C_dispatch_details'),
]