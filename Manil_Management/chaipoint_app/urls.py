from django.urls import path
from .views import *

urlpatterns = [   
    path('cp_dashboard', cp_dashboard, name='cp_dashboard'),
    path('C_order_table', C_order_table, name='C_order_table'),
    path('order_view/<str:ord_no>',order_view,name='order_view'),
    path('C_dispatch_details', C_dispatch_details, name='C_dispatch_details'),
]