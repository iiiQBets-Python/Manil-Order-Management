from django.urls import path
from .views import *

urlpatterns = [   
    path('c_notifications/fetch/', c_fetch_notifications, name='c_fetch_notifications'),  
    path('Client_dashboard', Client_dashboard, name='Client_dashboard'),
    path('client_report', client_report, name='client_report'),
    path('client_emails', client_emails, name='client_emails'),
    path('order_table', order_table, name='order_table'),
    path('client_order_view/<str:ord_no>',client_order_view,name='client_order_view'),
    path('edit_order_table', edit_order_table, name='edit_order_table'),
    path('Client_dispatch', Client_dispatch, name='Client_dispatch'),
    path('received_view/<str:ord_no>',received_view,name='received_view'),
    path('remarks_view/<str:ord_no>',remarks_view,name='remarks_view'),
    path('client_ticket', client_ticket,name='client_ticket'),
    path('c_ticket_view/<str:ticket_num>',c_ticket_view,name='c_ticket_view'),
    path('close_ticket/<str:ticket_num>', close_ticket, name='close_ticket'),
    path('edit_ticket/<str:id>', edit_ticket, name='edit_ticket'),
    path('invoice_table', invoice_table, name='invoice_table'),
    path('client_invoice_view/<str:ord_no>', client_invoice_view, name='client_invoice_view'),
    path('download_invoice/<str:ord_no>', download_invoice, name='download_invoice'),
    path('c_order_remarks', c_order_remarks, name='c_order_remarks'),
    path('c_order_remarks_view/<str:ord_no>', c_order_remarks_view, name='c_order_remarks_view' ),

    

    path('add_user', add_user, name='add_user'),
    path('edit_user/<str:id>', edit_user, name='edit_user'),
    path('c_profile/<str:user_id>/', c_user_profile, name='c_user_profile'),

    path('get-order-details/<str:order_number>/', get_order_details, name='get_order_details'),


    path('delete_user/<str:id>', delete_user, name='delete_user'),
    path('delete_c_order/<str:order_number>', delete_c_order, name='delete_c_order'),
    path('delete_c_dispatch/<str:id>', delete_c_dispatch, name='delete_c_dispatch'),
    path('delete_c_invoice/<str:id>', delete_c_invoice, name='delete_c_invoice'),
    path('delete_c_order_remark/<str:id>', delete_c_order_remark, name='delete_c_order_remark'),
    path('delete_c_robot_ticket/<str:id>', delete_c_robot_ticket, name='delete_c_robot_ticket'),
    
    path('Client_Reorder_dispatch', Client_Reorder_dispatch, name='Client_Reorder_dispatch'),
    path('re_received_view/<str:ord_no>',re_received_view,name='re_received_view'),
]