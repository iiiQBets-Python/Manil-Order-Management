from django.urls import path
from .views import *

urlpatterns = [   
      
    path('Client_dashboard', Client_dashboard, name='Client_dashboard'),
    path('client_report', client_report, name='client_report'),
    path('order_table', order_table, name='order_table'),
    path('Client_dispatch', Client_dispatch, name='Client_dispatch'),
    path('received_view/<str:ord_no>',received_view,name='received_view'),
    path('remarks_view/<str:ord_no>',remarks_view,name='remarks_view'),
    path('client_ticket', client_ticket,name='client_ticket'),
    path('invoice_table', invoice_table, name='invoice_table'),
    path('client_invoice_view/<str:ord_no>', client_invoice_view, name='client_invoice_view'),
    path('download_invoice/<str:ord_no>', download_invoice, name='download_invoice'),

    path('add_user', add_user, name='add_user'),
    path('edit_user/<str:id>', edit_user, name='edit_user'),
    
]