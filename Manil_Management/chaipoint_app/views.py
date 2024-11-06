

from Manil_Management.imports import *
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect

def cp_dashboard(request):
    user_id = request.session.get('user_id')
    data = chai_point_user.objects.get(user_id=user_id)

    # Fetch all orders
    m_orders = manil_order.objects.all()

    # Calculate counts
    total_orders = m_orders.count()
    total_dispatches = m_orders.filter(status='Dispatched').count()
    delivered_orders = m_orders.filter(status='Delivered').count()
    pending_deliveries = total_orders - (total_dispatches + delivered_orders)

    context = {
        'data': data,
        'total_orders': total_orders,
        'total_dispatches': total_dispatches,
        'pending_deliveries': pending_deliveries,
        'delivered_orders': delivered_orders,
    }

    return render(request, 'chaipoint_temp/cp_dashboard.html', context)


def C_order_table(request):
    user_id = request.session.get('user_id')
    data = chai_point_user.objects.get(user_id = user_id)

    m_orders = manil_order.objects.all()

    context = {
        'data':data, 'm_orders':m_orders
    }

    return render (request, 'chaipoint_temp/order_table.html', context)

def C_dispatch_details(request):
    user_id = request.session.get('user_id')
    data = chai_point_user.objects.get(user_id = user_id)

    dispatch = Despatch_Details.objects.all()

    context = {'data':data, 'dispatch':dispatch}

    return render(request, 'chaipoint_temp/chaipoint_dispatch.html', context)

def order_view(request, ord_no):    
    user_id = request.session.get('user_id')
    data = chai_point_user.objects.get(user_id = user_id)
 
    order = manil_order.objects.get(process_num = ord_no)
    ord_det = manil_order_details.objects.filter(process_num = ord_no)

    c_order = client_order.objects.get(order_number=order.order_number)

    client_det = Client_Master.objects.get(client_id = order.client_id)
    mat_list = Material_Master.objects.all()
    
    dispatch = Despatch_Details.objects.all()

    context = {'data':data, 'order':order, 'client_det':client_det, 'ord_det':ord_det, 'mat_list':mat_list, 'c_order':c_order , 'dispatch':dispatch}
    
    if request.method == 'POST':
        process_num = request.POST.get('process_number')
        client_id = request.POST.get('client_id')
        client_name = request.POST.get('client_name')
        exp_del_dt = request.POST.get('expected_delivery_date')

        if dispatch.exists():            
            last_name = dispatch.last().dispatch_lr_num                     
            pre = last_name[:-3]  
            suf = int(last_name[-3:])                        
            new_suf = suf + 1
                    
            new_suffix = f"{new_suf:03}"        
            new_lr_value = pre + new_suffix
        else:           
            new_lr_value = 'DLR001'

        new_dispatch = Despatch_Details(
            process_num = process_num,
            process_date = order.creation_date,
            client_id = client_id,
            client_name = client_name,
            order_number = order.order_number,
            order_date = order.order_date,
            dispatch_date = timezone.now() + timedelta(hours=5, minutes=30),
            dispatch_lr_num = new_lr_value,
            exp_del_dt = exp_del_dt,
            creation_date =  timezone.now() + timedelta(hours=5, minutes=30),
            created_by = data.user_id
        )
        new_dispatch.save()

        order.status = "Dispatched"
        order.save()

        c_order.status = "Dispatched"
        c_order.save()
        
        success_msg = 'Order Dispatched Succesfully.'
        
        return render (request, 'chaipoint_temp/order_view.html', {'data':data, 'order':order, 'client_det':client_det, 'ord_det':ord_det, 'mat_list':mat_list, 'c_order':c_order , 'dispatch':dispatch,'success_msg':success_msg})

    return render (request, 'chaipoint_temp/order_view.html', context)