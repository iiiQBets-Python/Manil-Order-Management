from django.urls import path
from .views import *

urlpatterns = [   
    path('forgot_password', forgot_password, name='forgot_password'),
    path('base', base, name='base'),
    path('manil_master', manil_master, name='manil_master'),
    path('Client_master', Client_master, name='Client_master'),  
    path('get_sname_matches', get_sname_matches, name='get_sname_matches'), 

    path('manil_dashboard', manil_dashboard, name='manil_dashboard'),

    path('cust_user_master', cust_user_master, name='cust_user_master'),
    
    
    
    path('material_master', material_master, name='material_master'),
    path('material_cost', material_cost, name='material_cost'),
    path('manil_user', manil_user, name='manil_user'),
    path('manil_order', manil_order, name='manil_order'),
    path('client_order', client_order, name='client_order'),
    path('manil_dispatch',manil_dispatch, name='manil_dispatch'),
    path('chaipoint_user', chaipoint_user, name='chaipoint_user'),
    path('manil_ticket', manil_ticket, name='manil_ticket'),
    path('robo_master', robo_master, name='robo_master'),
    path('robo_details', robo_details, name='robo_details'),
]