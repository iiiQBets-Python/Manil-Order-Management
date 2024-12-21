from django.urls import path
from .views import *

urlpatterns = [   
    path('forgot_password', forgot_password, name='forgot_password'),
    path('base', base, name='base'),
    path('manil_master', manil_master, name='manil_master'),
    path('manil_emails', manil_emails, name='manil_emails'),
    path('Client_master', Client_master, name='Client_master'),  
    path('get_sname_matches', get_sname_matches, name='get_sname_matches'), 

    path('manil_dashboard', manil_dashboard, name='manil_dashboard'),

    path('cust_user_master', cust_user_master, name='cust_user_master'),
    
    
    
    path('material_master', material_master, name='material_master'),
    path('material_cost', material_cost, name='material_cost'),
    path('manil_user', manil_user, name='manil_user'),
    path('m_profile/<str:user_id>/', m_user_profile, name='m_user_profile'),
    path('manil_order_', manil_order_, name='manil_order_'),
    path('client_order_', client_order_, name='client_order_'),
    path('c_order_view/<str:ord_no>',c_order_view,name='c_order_view'),
    path('ticket_view/<str:ticket_num>',ticket_view,name='ticket_view'),
    path('manil_dispatch',manil_dispatch, name='manil_dispatch'),
    path('order_remarks', order_remarks, name='order_remarks'),
    path('order_remarks_view/<str:ord_no>', order_remarks_view, name='order_remarks_view'),
    path('chaipoint_user', chaipoint_user, name='chaipoint_user'),
    path('manil_ticket', manil_ticket, name='manil_ticket'),
    path('robo_master', robo_master, name='robo_master'),
    path('robo_details', robo_details, name='robo_details'),

    path('invoice_preview/<str:ord_no>',invoice_preview,name='invoice_preview'),
    path('m_invoice_table', m_invoice_table, name='m_invoice_table'),
    path('m_invoice_view/<str:ord_no>', m_invoice_view, name='m_invoice_view'),
    path('m_download_invoice/<str:ord_no>', m_download_invoice, name='m_download_invoice'),


    path('edit_manil_user/<str:id>', edit_manil_user, name='edit_manil_user'),
    path('edit_client_master/<str:id>', edit_client_master, name='edit_client_master'),
    path('edit_cust_user/<str:id>', edit_cust_user, name='edit_cust_user'),
    path('edit_chaipoint_user/<str:id>', edit_chaipoint_user, name='edit_chaipoint_user'),
    path('edit_material_master/<str:id>',edit_material_master,name='edit_material_master'),
    path('edit_material_cost/<str:id>', edit_material_cost, name='edit_material_cost'),
    path('edit_robot_master/<str:id>', edit_robot_master, name='edit_robot_master'),
    path('edit_robo_details/<str:id>', edit_robo_details, name='edit_robo_details'),


    path('delete_manil_user/<str:id>', delete_manil_user, name='delete_manil_user'),
    path('delete_client_master/<str:id>', delete_client_master, name='delete_client_master'),
    path('delete_client_user/<str:id>', delete_client_user, name='delete_client_user'),
    path('delete_chaipoint_user/<str:id>', delete_chaipoint_user, name='delete_chaipoint_user'),
    path('delete_material/<str:id>', delete_material, name='delete_material'),
    path('delete_material_cost/<str:id>', delete_material_cost, name='delete_material_cost'),
    path('delete_client_order/<str:order_number>', delete_client_order, name='delete_client_order'),
    path('delete_manil_order/<str:process_num>', delete_manil_order, name='delete_manil_order'),
    path('delete_m_dispatch/<str:id>', delete_m_dispatch, name='delete_m_dispatch'),
    path('delete_invoice/<str:id>', delete_invoice, name='delete_invoice'),
    path('delete_order_remark/<str:id>', delete_order_remark, name='delete_order_remark'),
    path('delete_robot_ticket/<str:id>', delete_robot_ticket, name='delete_robot_ticket'),
    path('delete_robot/<str:id>', delete_robot, name='delete_robot'),
    path('delete_robot_details<str:id>', delete_robot_details, name='delete_robot_details')
    

]

