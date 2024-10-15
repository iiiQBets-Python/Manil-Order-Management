from Manil_Management.imports import *




def Client_dashboard(request):

    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id = user_id)   

    return render(request, 'customer_temp/Client_dashboard.html', {'data':data})


def order_table(request):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id = user_id)   

    order_list = client_order.objects.all()       

    return render (request, 'customer_temp/order_table.html', {'data':data, 'order_list':order_list})




def client_report(request):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id = user_id)   

    return render(request, 'customer_temp/client_report.html', {'data':data})


def Client_dispatch(request):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id = user_id)   

    return render (request, 'customer_temp/Client_dispatch.html', {'data':data})

def maintenance_details(request):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id = user_id)   

    return render (request, 'customer_temp/maintenance_details.html', {'data':data})

# chaipoint views

