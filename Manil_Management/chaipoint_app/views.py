

from Manil_Management.imports import *
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

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


    user_id = request.session.get('user_id')
    data = chai_point_user.objects.get(user_id=user_id)

    cp_user = chai_point_user.objects.all()
    context = {'data': data, 'cp_user': cp_user}

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email_id = request.POST.get('email_id')
        role = request.POST.get('role')                

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        context_2 = {
            'first_name': first_name, 'last_name': last_name, 'phone_number': phone_number, 
            'email_id': email_id, 'role': role
        }

        if password != confirm_password:
            messages.error(request, 'Password mismatch, Please try again.')      
            return render(request, 'manil_temp/chaipoint_user.html', { **context, **context_2 })
        
        if cp_user.exists():            
            last_num = cp_user.last().user_id                       
            pre = last_num[:-3]  
            suf = int(last_num[-3:]) 
            new_suf = suf + 1 
            
            if new_suf > 999:                
                new_suffix = f"{new_suf}" 
            else:
                new_suffix = f"{new_suf:03}"             
            new_user_id = pre + new_suffix
        else:           
            new_user_id = 'CPU001' 

        cp_user_new = chai_point_user(
            user_id=new_user_id,
            first_name=first_name,
            last_name=last_name,            
            role=role,            
            email_id=email_id,
            phone_number=phone_number,
            password=password,
            pwd_date=timezone.now() + timedelta(hours=5, minutes=30),
            creation_date=timezone.now() + timedelta(hours=5, minutes=30),
            created_by=data.first_name
        )
        cp_user_new.save()              

        cp_user_pwd = chai_point_user_pwd(
            user_id = new_user_id,
            first_name = first_name,
            password = password
        )       
        cp_user_pwd.save() 
        
        messages.success(request, 'Chai Point User added successfully.')
        return redirect('chaipoint_user')
        
    return render (request, 'chaipoint_temp/c_add_user.html', context)


def cp_order_table(request):
    user_id = request.session.get('user_id')
    data = chai_point_user.objects.get(user_id = user_id)

    m_orders = manil_order.objects.all()

    context = {
        'data':data, 'm_orders':m_orders
    }

    return render (request, 'chaipoint_temp/order_table.html', context)

def cp_dispatch_details(request):
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
            process_num = order.process_num,
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

        messages.success(request, 'Order Dispatched Succesfully.')
        return redirect('C_dispatch_details')
        
    return render (request, 'chaipoint_temp/order_view.html', context)