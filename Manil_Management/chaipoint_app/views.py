

from Manil_Management.imports import *
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from manil_app.context_processors import global_context

from django.http import JsonResponse
from django.urls import reverse


def cp_fetch_notifications(request):
    # Initialize counts and notification lists
    cp_order_count = manil_order.objects.filter(status="Order Placed").count()
    
    cp_notifications = Chaipoint_Notification.objects.filter(is_read=False)
    
    return JsonResponse({
        'status': 'success',
        'cp_order_count': cp_order_count,
        'cp_notifications': list(cp_notifications.values('id', 'title', 'message')),
        'cp_unread_count': cp_notifications.count(),
    })

def mark_chaipoint_notification_as_read(request, order_number):
    notification = get_object_or_404(Chaipoint_Notification, order_number=order_number)

    if not notification.is_read:
        notification.is_read = True
        notification.save()

    return redirect(reverse('order_view', args=[order_number]))

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

def cp_emails(request):
    user_id = request.session.get('user_id')
    data = chai_point_user.objects.get(user_id = user_id)
    emails = Chaipoint_emails.objects.first()

    email_data_exists = any([
        emails.username1, emails.email1,
        emails.username2, emails.email2,
        emails.username3, emails.email3,
        emails.username4, emails.email4,
        emails.username5, emails.email5
    ]) if emails else False


    if emails is None:
        emails = Chaipoint_emails()

    
    if request.method == 'POST':        
        
        emails.username1 = request.POST.get('username1')
        emails.email1 = (request.POST.get('email1'))
        emails.username2 = request.POST.get('username2')
        emails.email2 = (request.POST.get('email2'))
        emails.username3 = request.POST.get('username3')
        emails.email3 = (request.POST.get('email3'))
        emails.username4 = request.POST.get('username4')
        emails.email4 = (request.POST.get('email4'))
        emails.username5 = request.POST.get('username5')
        emails.email5 = (request.POST.get('email5'))
       
        emails.save()

        return redirect('cp_emails')
    
    
    return render (request, 'chaipoint_temp/cp_emails.html', {'data':data, 'emails':emails, 'email_data_exists':email_data_exists})

def cp_add_user(request):
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
            return render(request, 'chaipoint_temp/c_add_user.html', { **context, **context_2 })
        
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
        return redirect('cp_add_user')
        
    return render (request, 'chaipoint_temp/cp_add_user.html', context)


def cp_user_profile(request, user_id):
    data = chai_point_user.objects.get(user_id=user_id)
    context = {'data': data}
    return render(request, 'chaipoint_temp/cp_user_profile.html', context)

def edit_cp_user(request, id):
    user_id = request.session.get('user_id')
    data = chai_point_user.objects.get(user_id=user_id)

    cp_user = get_object_or_404(chai_point_user, id=id)

    if request.method == 'POST':
        cp_user.first_name = request.POST.get('edit_first_name')
        cp_user.last_name = request.POST.get('edit_last_name')
        cp_user.phone_number = request.POST.get('edit_phone_number')
        cp_user.email_id = request.POST.get('edit_email_id')
        cp_user.role = request.POST.get('edit_role')
        cp_user.updated_date = timezone.now() + timedelta(hours=5, minutes=30)
        cp_user.updated_by = data.first_name 

        cp_user.save()

        messages.success(request, 'Chaipoint User details updated successfully.')
        return redirect('cp_add_user')

    return render(request, 'chaipoint_temp/cp_add_user.html', {'data': data, 'cp_user': cp_user})

def cp_order_table(request):
    user_id = request.session.get('user_id')
    data = chai_point_user.objects.get(user_id = user_id)

    m_orders = manil_order.objects.all()

    context = {
        'data':data, 'm_orders':m_orders
    }

    return render (request, 'chaipoint_temp/order_table.html', context)

def re_cp_order_table(request):
    user_id = request.session.get('user_id')
    data = chai_point_user.objects.get(user_id = user_id)

    m_orders = Re_manil_order.objects.all()

    context = {
        'data':data, 'm_orders':m_orders
    }

    return render (request, 'chaipoint_temp/re_order_table.html', context)

def re_order_view(request, ord_no):    

    user_id = request.session.get('user_id')
    data = chai_point_user.objects.get(user_id=user_id)
 
    order = Re_manil_order.objects.get(order_number=ord_no)
    
    ord_det = Re_manil_order_details.objects.filter(process_num=order.process_num)
    
    try:
        c_order = client_order.objects.get(order_number=order.order_number)
    except:
        c_order= None

    client_det = Client_Master.objects.get(client_id=order.client_id)
    mat_list = Material_Master.objects.all()
    
    dispatch = Re_Despatch_Details.objects.filter(order_number = order.order_number)

    cp_notification = Chaipoint_Notification.objects.get(order_number=ord_no)

    context = {
        'data': data,
        'order': order,
        'client_det': client_det,
        'ord_det': ord_det,
        'mat_list': mat_list,
        'c_order': c_order,
        'dispatch': dispatch,
        'cp_notification':cp_notification,
    }
    
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        client_name = request.POST.get('client_name')
        exp_del_dt = request.POST.get('expected_delivery_date')

        if dispatch.exists():            
            last_name = dispatch.last().dispatch_lr_num                     
            prefix, suffix = last_name.split('_R')  
            numeric = int(suffix) + 1  
            new_re_lr_no = f"{prefix}_R{numeric}"
        else:           
            new_re_lr_no = 'DLR_R1'

        # Save new dispatch details
        new_dispatch = Re_Despatch_Details(
            process_num=order.process_num,
            process_date=order.creation_date,
            client_id=client_id,
            client_name=client_name,
            order_number=order.order_number,
            order_date=order.order_date,
            dispatch_date=timezone.now() + timedelta(hours=5, minutes=30),
            dispatch_lr_num=new_re_lr_no,
            exp_del_dt=exp_del_dt,
            creation_date=timezone.now() + timedelta(hours=5, minutes=30),
            created_by=data.user_id
        )
        new_dispatch.save()

        # Update order and client order statuses
        order.status = "Dispatched"
        order.save()

        cp_notification.is_read = True
        cp_notification.save()

        notification_title = "Order Confirmation"
        notification_message = f"We are pleased to inform you, the order with (Order No: {order.re_order_number}) was successfully dispatched on {timezone.now().strftime('%d-%m-%Y at %H:%M')}. By {data.first_name}."


        # Create a new notification for the logged-in user
        c_notification = Client_Notification(
            order_number = order.re_order_number,
            message=notification_message,
            title = notification_title
        )
        c_notification.save()    

         # Prepare order details for email
        order_details_rows = ""
        for idx, detail in enumerate(ord_det, start=1):
            order_details_rows += f"""
            <tr>
                <td>{idx}</td>
                <td>{detail.material_name}</td>
                <td>{detail.uom}</td>
                <td>{detail.qty}</td>
                <td>{detail.base_price}</td>
                <td>{detail.gst_rate}%</td>
                <td>{detail.gst_amt}</td>
                <td>{detail.sub_total}</td>
            </tr>
            """

        email_body = f"""
        <p>Dear Manil Team,</p>
        <p>The following order has been dispatched:</p>

        <h3>Dispatch Summary</h3>
        <p><strong>Dispatch Number:</strong> {new_re_lr_no}</p>
        <p><strong>Order Number:</strong> {order.re_order_number}</p>
        <p><strong>Dispatch Date:</strong> {timezone.now().strftime('%Y-%m-%d')}</p>
        <p><strong>Expected Delivery Date:</strong> {exp_del_dt}</p>

        <h3>Order Details</h3>
        <table border="1" style="border-collapse: collapse; width: 100%; text-align: left;">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Material Name</th>
                    <th>UOM</th>
                    <th>Quantity</th>
                    <th>Base Price</th>
                    <th>GST Rate</th>
                    <th>GST Amount</th>
                    <th>Subtotal</th>
                </tr>
            </thead>
            <tbody>
                {order_details_rows}
            </tbody>
        </table>
        <p>Thank you!</p>
        """

        manil_email_obj = Manil_emails.objects.first()

        # Extract the email fields from the first entry (if it exists)
        if manil_email_obj:
            manil_emails = [
                manil_email_obj.email1,
                manil_email_obj.email2,
                manil_email_obj.email3,
                manil_email_obj.email4,
                manil_email_obj.email5
            ]
        else:
            manil_emails = []

        chaipoint_email_obj = Chaipoint_emails.objects.first()

        # Extract the email fields from the first entry (if it exists)
        if chaipoint_email_obj:
            chaipoint_emails = [
                chaipoint_email_obj.email1,
                chaipoint_email_obj.email2,
                chaipoint_email_obj.email3,
                chaipoint_email_obj.email4,
                chaipoint_email_obj.email5
            ]
        else:
            chaipoint_emails = []  

        client_emails = []
        client_email_objs = Client_emails.objects.filter(client_id=order.client_id)  
        for client_email_obj in client_email_objs:
            for i in range(1, 6):  # Loop through email1 to email5 fields
                email_field = f'email{i}'
                email = getattr(client_email_obj, email_field, None)
                if email:
                    client_emails.append(email)

        recipient_list = manil_emails + chaipoint_emails + client_emails

        # Send email
        email = EmailMessage(
            subject='Order Dispatched Notification',
            body=email_body,
            from_email=settings.EMAIL_HOST_USER,
            to=recipient_list,
        )
        email.content_subtype = 'html'
        email.send(fail_silently=False)

    
        messages.success(request, 'Order Dispatched Successfully.')
        return redirect('re_cp_dispatch_details')
        
    return render(request, 'chaipoint_temp/re_order_view.html', context)


def cp_dispatch_details(request):
    user_id = request.session.get('user_id')
    data = chai_point_user.objects.get(user_id = user_id)

    dispatch = Despatch_Details.objects.all()

    context = {'data':data, 'dispatch':dispatch}

    return render(request, 'chaipoint_temp/chaipoint_dispatch.html', context)

def re_cp_dispatch_details(request):
    user_id = request.session.get('user_id')
    data = chai_point_user.objects.get(user_id = user_id)

    dispatch = Re_Despatch_Details.objects.all()

    context = {'data':data, 'dispatch':dispatch}

    return render(request, 'chaipoint_temp/re_chaipoint_dispatch.html', context)

def order_view(request, ord_no):    

    user_id = request.session.get('user_id')
    data = chai_point_user.objects.get(user_id=user_id)
 
    order = manil_order.objects.get(order_number=ord_no)
    
    ord_det = manil_order_details.objects.filter(process_num=order.process_num)
    
    try:
        c_order = client_order.objects.get(order_number=order.order_number)
    except:
        c_order= None

    client_det = Client_Master.objects.get(client_id=order.client_id)
    mat_list = Material_Master.objects.all()
    
    dispatch = Despatch_Details.objects.all()

    cp_notification = Chaipoint_Notification.objects.get(order_number=ord_no)

    context = {
        'data': data,
        'order': order,
        'client_det': client_det,
        'ord_det': ord_det,
        'mat_list': mat_list,
        'c_order': c_order,
        'dispatch': dispatch,
        'cp_notification':cp_notification,
    }
    
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

        # Save new dispatch details
        new_dispatch = Despatch_Details(
            process_num=order.process_num,
            process_date=order.creation_date,
            client_id=client_id,
            client_name=client_name,
            order_number=order.order_number,
            order_date=order.order_date,
            dispatch_date=timezone.now() + timedelta(hours=5, minutes=30),
            dispatch_lr_num=new_lr_value,
            exp_del_dt=exp_del_dt,
            creation_date=timezone.now() + timedelta(hours=5, minutes=30),
            created_by=data.user_id
        )
        new_dispatch.save()

        # Update order and client order statuses
        order.status = "Dispatched"
        order.save()

        if c_order:
            c_order.status = "Dispatched"
            c_order.save()

        cp_notification.is_read = True
        cp_notification.save()

        notification_title = "Order Confirmation"
        notification_message = f"We are pleased to inform you, the order with (Order No: {order.order_number}) was successfully dispatched on {timezone.now().strftime('%d-%m-%Y at %H:%M')}. By {data.first_name}."


        # Create a new notification for the logged-in user
        c_notification = Client_Notification(
            order_number = order.order_number,
            message=notification_message,
            title = notification_title
        )
        c_notification.save()

        # Prepare order details for email
        order_details_rows = ""
        for idx, detail in enumerate(ord_det, start=1):
            order_details_rows += f"""
            <tr>
                <td>{idx}</td>
                <td>{detail.material_name}</td>
                <td>{detail.uom}</td>
                <td>{detail.qty}</td>
                <td>{detail.base_price}</td>
                <td>{detail.gst_rate}%</td>
                <td>{detail.gst_amt}</td>
                <td>{detail.sub_total}</td>
            </tr>
            """

        email_body = f"""
        <p>Dear Manil Team,</p>
        <p>The following order has been dispatched:</p>

        <h3>Dispatch Summary</h3>
        <p><strong>Dispatch Number:</strong> {new_lr_value}</p>
        <p><strong>Order Number:</strong> {order.order_number}</p>
        <p><strong>Dispatch Date:</strong> {timezone.now().strftime('%Y-%m-%d')}</p>
        <p><strong>Expected Delivery Date:</strong> {exp_del_dt}</p>

        <h3>Order Details</h3>
        <table border="1" style="border-collapse: collapse; width: 100%; text-align: left;">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Material Name</th>
                    <th>UOM</th>
                    <th>Quantity</th>
                    <th>Base Price</th>
                    <th>GST Rate</th>
                    <th>GST Amount</th>
                    <th>Subtotal</th>
                </tr>
            </thead>
            <tbody>
                {order_details_rows}
            </tbody>
        </table>
        <p>Thank you!</p>
        """

        manil_email_obj = Manil_emails.objects.first()

        # Extract the email fields from the first entry (if it exists)
        if manil_email_obj:
            manil_emails = [
                manil_email_obj.email1,
                manil_email_obj.email2,
                manil_email_obj.email3,
                manil_email_obj.email4,
                manil_email_obj.email5
            ]
        else:
            manil_emails = []

        chaipoint_email_obj = Chaipoint_emails.objects.first()

        # Extract the email fields from the first entry (if it exists)
        if chaipoint_email_obj:
            chaipoint_emails = [
                chaipoint_email_obj.email1,
                chaipoint_email_obj.email2,
                chaipoint_email_obj.email3,
                chaipoint_email_obj.email4,
                chaipoint_email_obj.email5
            ]
        else:
            chaipoint_emails = []  

        client_emails = []
        client_email_objs = Client_emails.objects.filter(client_id=order.client_id)  
        for client_email_obj in client_email_objs:
            for i in range(1, 6):  # Loop through email1 to email5 fields
                email_field = f'email{i}'
                email = getattr(client_email_obj, email_field, None)
                if email:
                    client_emails.append(email)

        recipient_list = manil_emails + chaipoint_emails + client_emails

        # Send email
        email = EmailMessage(
            subject='Order Dispatched Notification',
            body=email_body,
            from_email=settings.EMAIL_HOST_USER,
            to=recipient_list,
        )
        email.content_subtype = 'html'
        email.send(fail_silently=False)

        messages.success(request, 'Order Dispatched Successfully.')
        return redirect('cp_dispatch_details')
        
    return render(request, 'chaipoint_temp/order_view.html', context)

def edit_dispatch(request, id):
    user_id = request.session.get('user_id')
    data = chai_point_user.objects.get(user_id = user_id)

    dispatch =get_object_or_404(Despatch_Details, id=id) 
    
    context={
        'data':data, 'dispatch':dispatch
    }
    if request.method == 'POST':
        dispatch.exp_del_dt = request.POST.get('edit_expected_delivery_date')
        dispatch.save()

        messages.success(request, 'Order Dispatched details updated Succesfully.')
        return redirect('cp_dispatch_details')    
    
    return render (request, 'chaipoint_temp/order_view.html', context) 

def delete_cp_user(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(chai_point_user, user_id=user_id)
    
    cp_user = get_object_or_404(chai_point_user, id=id)
    cp_user.delete()

    messages.success(request, 'Chaipoint user is Deletd Successfully')
    return redirect('chaipoint_user')

def delete_cp_order(request, process_num):
    user_id = request.session.get('user_id')
    data = get_object_or_404(chai_point_user, user_id=user_id)
    
    m_order = get_object_or_404(manil_order, process_num=process_num)
    m_order.delete()

    m_order_details = manil_order_details.objects.filter(process_num=process_num)
    m_order_details.delete()

    c_order = get_object_or_404(client_order, order_number=m_order.order_number)
    c_order.status = "Order Placed"
    c_order.save()

    messages.success(request, 'Manil Order is Deleted Successfully')
    return redirect('manil_order_')

def delete_cp_dispatch(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(chai_point_user, user_id=user_id)
    
    m_dispatch = get_object_or_404(Despatch_Details, id=id)
    m_dispatch.delete()

    m_order = get_object_or_404(manil_order, process_num=m_dispatch.process_num)
    m_order.status = "Order Placed"
    m_order.save()

    c_order = get_object_or_404(client_order, order_number=m_dispatch.order_number)
    c_order.status = "In Progress"
    c_order.save()

    messages.success(request, 'Dispatch details are Deleted Successfully')
    return redirect('manil_dispatch')