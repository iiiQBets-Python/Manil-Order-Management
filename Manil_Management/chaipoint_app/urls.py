from django.urls import path
from .views import *

urlpatterns = [   
    path('cp_notifications/fetch/', cp_fetch_notifications, name='cp_fetch_notifications'),
    path('cp_dashboard', cp_dashboard, name='cp_dashboard'),
    path('cp_add_user',cp_add_user,name='cp_add_user'),
    path('cp_emails', cp_emails, name='cp_emails'),
    path('cp_profile/<str:user_id>/', cp_user_profile, name='cp_user_profile'),
    path('edit_cp_user/<str:id>', edit_cp_user, name='edit_cp_user'),
    path('cp_order_table', cp_order_table, name='cp_order_table'),
    path('order_view/<str:ord_no>',order_view,name='order_view'),
    path('cp_dispatch_details', cp_dispatch_details, name='cp_dispatch_details'),
    path('edit_dispatch/<str:id>', edit_dispatch, name='edit_dispatch'),


    path('delete_cp_user/<str:id>', delete_cp_user, name='delete_cp_user'),
    path('delete_cp_order/<str:process_num>', delete_cp_order, name='delete_cp_order'),
    path('delete_cp_dispatch/<str:id>', delete_cp_dispatch, name='delete_cp_dispatch'),


    path('re_cp_order_table', re_cp_order_table, name='re_cp_order_table'),
    path('re_order_view/<str:ord_no>',re_order_view,name='re_order_view'),
    path('re_cp_dispatch_details', re_cp_dispatch_details, name='re_cp_dispatch_details'),
]