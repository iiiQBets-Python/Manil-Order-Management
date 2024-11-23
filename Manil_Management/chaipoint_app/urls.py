from django.urls import path
from .views import *

urlpatterns = [   
    path('cp_dashboard', cp_dashboard, name='cp_dashboard'),
    path('cp_order_table', cp_order_table, name='cp_order_table'),
    path('order_view/<str:ord_no>',order_view,name='order_view'),
    path('cp_dispatch_details', cp_dispatch_details, name='cp_dispatch_details'),
]