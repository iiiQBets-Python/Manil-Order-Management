

from Manil_Management.imports import *

def C_order_table(request):
    return render (request, 'chaipoint_temp/order_table.html')

def C_dispatch_details(request):
    return render(request, 'chaipoint_temp/chaipoint_dispatch.html')