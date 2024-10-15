from django.urls import path
from .views import *

urlpatterns = [   
      
    path('Client_dashboard', Client_dashboard, name='Client_dashboard'),
    path('client_report', client_report, name='client_report'),
    path('order_table', order_table, name='order_table'),
    path('Client_dispatch',Client_dispatch, name='Client_dispatch'),
    path('maintenance_details',maintenance_details,name='maintenance_details'),
    
]