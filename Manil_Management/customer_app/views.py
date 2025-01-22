from Manil_Management.imports import *
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from num2words import num2words
from django.http import HttpResponse, JsonResponse



def c_fetch_notifications(request):
    
    c_notifications = Client_Notification.objects.filter(is_read=False)
    c_inv_notifications = Client_Inv_Notification.objects.filter(is_read=False)
    
    return JsonResponse({
        'status': 'success',
        'c_notifications': list(c_notifications.values('id', 'title', 'message')),
        'c_unread_count': c_notifications.count(),
        'c_inv_notifications': list(c_inv_notifications.values('id', 'title', 'message')),
        'c_inv_unread_count': c_inv_notifications.count(),
    })



def Client_dashboard(request):    
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id=user_id)

    # Fetch orders based on client ID
    orders = client_order.objects.filter(client_id=data.client_id)
    
    # Categorize orders
    total_orders = orders.count()
    received_orders = orders.filter(status__iexact='Delivered').count()
    pending_orders = orders.filter(status__iexact='Pending').count()
    remarked_orders = Order_Tickets.objects.filter(client_id=data.client_id).count()

    orders_last_5 = client_order.objects.filter(client_id=data.client_id).order_by('-id')[:5]

    # Fetch robot details
    robot_details = Robot_Details.objects.filter(client_id=data.client_id)

    return render(request, 'customer_temp/Client_dashboard.html', {
        'data': data,
        'orders': orders,
        'total_orders': total_orders,
        'received_orders': received_orders,
        'pending_orders': pending_orders,
        'remarked_orders': remarked_orders,
        'robot_details': robot_details,
        'orders_last_5':orders_last_5,
    })

def client_emails(request):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id=user_id)

   # Try to fetch the first 'Client_emails' object, or create a new one if none exist
    emails = Client_emails.objects.filter(client_id=data.client_id).first()

    email_data_exists = any([
        emails.username1, emails.email1,
        emails.username2, emails.email2,
        emails.username3, emails.email3,
        emails.username4, emails.email4,
        emails.username5, emails.email5
    ]) if emails else False

    if emails is None:
        emails = Client_emails(client_id=data.client_id)

    if request.method == 'POST':        
        emails.client_id = data.client_id
        
        emails.username1 = request.POST.get('username1')
        emails.email1 = request.POST.get('email1')
        emails.username2 = request.POST.get('username2')
        emails.email2 = request.POST.get('email2')
        emails.username3 = request.POST.get('username3')
        emails.email3 = request.POST.get('email3')
        emails.username4 = request.POST.get('username4')
        emails.email4 = request.POST.get('email4')
        emails.username5 = request.POST.get('username5')
        emails.email5 = request.POST.get('email5')
       
        emails.save()

        return redirect('client_emails')
    
    return render(request, 'customer_temp/client_emails.html', {'data': data, 'emails': emails, 'email_data_exists':email_data_exists})


def add_user(request):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id=user_id)

    client_m = Client_Master.objects.all()
    com_user = Client_user.objects.filter(client_id = data.client_id)

    context = {'data': data, 'client_m': client_m, 'com_user': com_user}

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email_id = request.POST.get('email_id')
        role = request.POST.get('role')        

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        context_2 = {
            'first_name': first_name, 'last_name': last_name, 'phone_number': phone_number, 'email_id': email_id, 
            'role': role,
        }

        # Merging the context dictionaries
        combined_context = {**context, **context_2}

        if password != confirm_password:
            messages.error(request, 'Password mismatch, Please try again.')
            return render(request, 'customer_temp/add_user.html', combined_context)

        

        try:
            exist_user = Client_user.objects.filter(client_id=data.client_id).last()

            prefix = exist_user.user_id.split('_u')[0]  
            numeric_part = exist_user.user_id.split('_u')[1]             
            new_number = str(int(numeric_part) + 1).zfill(len(numeric_part))            
            new_user_id = f"{prefix}_u{new_number}"

        except:
            exist_user = None
            new_user_id = f"{data.client_id}_u01"
        
        Client_user_new = Client_user(
            user_id=new_user_id,
            first_name=first_name,
            last_name=last_name,
            client_id=data.client_id,
            client_name=data.client_name,
            role=role,            
            email_id=email_id,
            phone_number=phone_number,
            password=password,
            pwd_date=timezone.now() + timedelta(hours=5, minutes=30),
            creation_date=timezone.now() + timedelta(hours=5, minutes=30),
            created_by=data.user_id
        )
        Client_user_new.save()              

        messages.success(request, 'Client User Added Successfully')
        return redirect('add_user')

    return render(request, 'customer_temp/add_user.html', context)

def c_user_profile(request, user_id):
    data = Client_user.objects.get(user_id=user_id)
    context = {'data': data}
    return render(request, 'customer_temp/c_user_profile.html', context)

def edit_user(request, id):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id=user_id)

    client_m = Client_Master.objects.all()
    com_user = get_object_or_404(Client_user, id=id)
    
    if request.method == 'POST':
        com_user.first_name = request.POST.get('edit_first_name')
        com_user.last_name = request.POST.get('edit_last_name')
        com_user.phone_number = request.POST.get('edit_phone_number')
        com_user.email_id = request.POST.get('edit_email_id')
        com_user.role = request.POST.get('edit_role')        

        com_user.updated_date = timezone.now() + timedelta(hours=5, minutes=30)
        com_user.updated_by = data.first_name 

        
        com_user.save()
        messages.success(request, 'Manil User details updated successfully.')
        return redirect('add_user')

    return render(request, 'customer_temp/add_user.html', {'data': data, 'client_m': client_m, 'com_user': com_user})

def order_table(request):
    
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id = user_id)   

    c_data = Client_Master.objects.get(client_id = data.client_id)

    order_list = client_order.objects.filter(client_id = data.client_id)       

    all_orders = client_order.objects.all()
    mat_list = Material_Master.objects.all()
    cost_det = Costing_Table.objects.filter(client_id = data.client_id) 

    if c_data.shipping_state.lower() == 'karnataka':
        inside = True        
    else:
        inside = False           

    context = {
        'c_data':c_data, 'data':data, 'order_list':order_list, 
        'all_orders':all_orders, 'mat_list':mat_list, 'cost_det':cost_det, 'inside':inside
    }


    if request.method == 'POST':
        
        no_of_sec = request.POST.get('no_of_sec')

        shipping_address = request.POST.get('shipping_address')
        shipping_city = request.POST.get('shipping_city')
        shipping_state = request.POST.get('shipping_state')
        shipping_pin = request.POST.get('shipping_pin')

        amt_in_words = request.POST.get('amt_in_words')
        grand_total = request.POST.get('grand_total')

        

        if all_orders.exists():            
            last_num = all_orders.last().order_number                       
            pre = last_num[:-3]  
            suf = int(last_num[-3:]) 
            new_suf = suf + 1 
            
            if new_suf > 999:                
                new_suffix = f"{new_suf}" 
            else:
                new_suffix = f"{new_suf:03}"             
            new_value = pre + new_suffix
        else:           
            new_value = 'ORD001' 

        
        for i in range(1, int(no_of_sec) + 1):            
            material_name = request.POST.get(f'material_name_{i}')
            hsn_code = request.POST.get(f'hsn_code_{i}')
            uom = request.POST.get(f'uom_{i}')
            qty = request.POST.get(f'qty_{i}')
            base_price = request.POST.get(f'base_price_{i}')
            gst_type = request.POST.get(f'gst_type_{i}')
            gst_rate = request.POST.get(f'gst_rate_{i}')
            gst_amt = request.POST.get(f'gst_amt_{i}')
            sub_total = request.POST.get(f'sub_total_{i}')

            

            order_details_n = client_order_details(
                order_number = new_value,
                material_name = material_name,
                hsn_code = hsn_code,
                uom = uom,
                qty = qty,
                base_price = base_price,
                gst_type = gst_type,
                gst_rate = gst_rate,
                gst_amt = round(float(gst_amt)),
                sub_total = round(float(sub_total))
            )
            order_details_n.save()

        client_order_new = client_order(
            client_id = data.client_id,
            client_name = data.client_name,
            po_authority=data.first_name + data.last_name,
            po_authority_date=timezone.now() + timedelta(hours=5, minutes=30),
            order_number = new_value,
            order_date = timezone.now() + timedelta(hours=5, minutes=30),
            creation_date = timezone.now() + timedelta(hours=5, minutes=30),
            created_by = data.first_name,
            grand_total = round(float(grand_total)),
            ammount_words = amt_in_words, 

            shipping_address = shipping_address,
            shipping_city = shipping_city,
            shipping_state = shipping_state,
            shipping_pin = shipping_pin,
            status = 'Order Placed'
        )
        client_order_new.save()

        notification_title = "Order Confirmation"
        notification_message = f"We are pleased to inform you, the order with (Order No: {new_value}) was successfully placed on {timezone.now().strftime('%d-%m-%Y at %H:%M')}. By {data.first_name}."


        # Create a new notification for the logged-in user
        m_notification = Manil_Notification(
            order_number = new_value,
            message=notification_message,
            title = notification_title
        )
        m_notification.save()

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
        
        # Fetch emails for the selected client_id from Client_emails
        client_emails = []
        client_email_objs = Client_emails.objects.filter(client_id=data.client_id)  
        for client_email_obj in client_email_objs:
            for i in range(1, 6):  # Loop through email1 to email5 fields
                email_field = f'email{i}'
                email = getattr(client_email_obj, email_field, None)
                if email:
                    client_emails.append(email)

        # Combine recipients
        email_recipients = manil_emails + client_emails

        # Prepare the order details table for the email body
        order_details_rows = ""
        for i in range(1, int(no_of_sec) + 1):
            material_name = request.POST.get(f'material_name_{i}')
            hsn_code = request.POST.get(f'hsn_code{i}')
            uom = request.POST.get(f'uom_{i}')
            qty = request.POST.get(f'qty_{i}')
            base_price = request.POST.get(f'base_price_{i}')
            gst_rate = request.POST.get(f'gst_rate_{i}')
            gst_amt = request.POST.get(f'gst_amt_{i}')
            sub_total = request.POST.get(f'sub_total_{i}')
            order_details_rows += f"""
            <tr>
                <td>{i}</td>
                <td>{material_name}</td>
                <td>{uom}</td>
                <td>{qty}</td>
                <td>{base_price}</td>
                <td>{gst_rate}%</td>
                <td>{gst_amt}</td>
                <td>{sub_total}</td>
            </tr>
            """

        # Compose the email body
        email_body = f"""
        <p>Dear {data.client_name},</p>
        <p>Your order has been placed successfully! Here are the details of your order:</p>

        <h3>Order Summary</h3>
        <p><strong>Order Number:</strong> {new_value}</p>
        <p><strong>Order Date:</strong> {(timezone.now() + timedelta(hours=5, minutes=30)).strftime('%d-%m-%Y %H:%M')}</p>

        <h3>Order Details</h3>
        <table border="1" style="border-collapse: collapse; width: 100%; text-align: left;">
            <thead>
                <tr>
                    <th>S.No</th>
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

        <p><strong>Total Amount :</strong> {grand_total}</p>
        <p><strong>Amount in Words:</strong> {amt_in_words}</p>

        <p>Thank you for your business!</p>
        """

        # Send the email
        email = EmailMessage(
            subject='Order Update',
            body=email_body,
            from_email=settings.EMAIL_HOST_USER,
            to=email_recipients,
        )
        email.content_subtype = 'html'
        email.encoding = 'utf-8'
        email.send(fail_silently=False)

        messages.success(request, 'Your order has been Placed.')
        return redirect('order_table')

    return render (request, 'customer_temp/order_table.html', context)


def client_order_view(request, ord_no):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id=user_id)

    all_orders = manil_order.objects.all()
    order = client_order.objects.get(order_number=ord_no)
    ord_det = client_order_details.objects.filter(order_number=ord_no)
    client_det = Client_Master.objects.get(client_id=order.client_id)
    mat_list = Material_Master.objects.all()
 

    context = {
        'data': data,
        'order': order,
        'ord_det': ord_det,
        'client_det':client_det,
        'mat_list': mat_list,
    }

    return render(request, 'customer_temp/order_view.html', context)



from django.http import JsonResponse 

def get_order_details(request, order_number):
    """
    Fetch and return order details based on the given order_number as a JSON response.
    """
    try:
        # Fetch the client_order instance
        order = get_object_or_404(client_order, order_number=order_number)
        
        # Fetch related order details
        order_details = client_order_details.objects.filter(order_number=order.order_number).values()

        # If no details found, return an error response
        if not order_details.exists():
            return JsonResponse({'error': 'No details found for this order'}, status=404)

        # Convert queryset to a list of dictionaries and return as JSON
        order_details_list = list(order_details)
        
        return JsonResponse(order_details_list, safe=False)

    except Exception as e:
        return JsonResponse({'error': f"Server error: {str(e)}"}, status=500)




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

def edit_order_table(request):
    if request.method == 'POST':
        # Fetch main order
        order_number = request.POST.get('edit_order_number')
        order = get_object_or_404(client_order, order_number=order_number)

        # Update main order fields
        order.shipping_address = request.POST.get('edit_shipping_address', '')
        order.shipping_city = request.POST.get('edit_shipping_city', '')
        order.shipping_state = request.POST.get('edit_shipping_state', '')
        order.shipping_pin = request.POST.get('edit_shipping_pin', '')
        order.save()

        # Update existing order details
        order_detail_ids = request.POST.getlist('order_detail_ids')  # Hidden input for detail IDs
        for detail_id in order_detail_ids:
            detail = get_object_or_404(client_order_details, id=detail_id, order=order)

            # Update the detail fields
            detail.material_name = request.POST.get(f'edit_material_name_{detail_id}', detail.material_name)
            detail.qty = request.POST.get(f'edit_qty_{detail_id}', detail.qty)
            detail.base_price = request.POST.get(f'edit_base_price_{detail_id}', detail.base_price)
            detail.gst_type = request.POST.get(f'edit_gst_type_{detail_id}', detail.gst_type)
            detail.gst_rate = request.POST.get(f'edit_gst_rate_{detail_id}', detail.gst_rate)
            detail.gst_amt = request.POST.get(f'edit_gst_amt_{detail_id}', detail.gst_amt)
            detail.sub_total = request.POST.get(f'edit_sub_total_{detail_id}', detail.sub_total)
            detail.save()

        # Add new order details
        new_details_count = int(request.POST.get('edit_no_of_sec', 0))  # Hidden input for new rows count
        for i in range(new_details_count):
            material_name = request.POST.get(f'new_material_name_{i}')
            if material_name:  # Avoid blank entries
                client_order_details.objects.create(
                    order=order,
                    material_name=material_name,
                    qty=request.POST.get(f'new_qty_{i}', 0),
                    base_price=request.POST.get(f'new_base_price_{i}', 0.0),
                    gst_type=request.POST.get(f'new_gst_type_{i}', ''),
                    gst_rate=request.POST.get(f'new_gst_rate_{i}', 0.0),
                    gst_amt=request.POST.get(f'new_gst_amt_{i}', 0.0),
                    sub_total=request.POST.get(f'new_sub_total_{i}', 0.0),
                )

        # Success message
        messages.success(request, 'Order updated successfully.')
        return redirect('order_table')  # Update with your actual redirection view name

    # If GET request, render an appropriate response (not expected in your case)
    return render(request, 'customer_temp/order_table.html')


def client_report(request):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id = user_id)   

    return render(request, 'customer_temp/client_report.html', {'data':data})

def Client_dispatch(request):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id = user_id)   
    
    dispatch = Despatch_Details.objects.filter(client_id=data.client_id)

    return render (request, 'customer_temp/Client_dispatch.html', {'data':data, 'dispatch':dispatch })

def Client_Reorder_dispatch(request):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id = user_id)   
    
    dispatch = Re_Despatch_Details.objects.filter(client_id=data.client_id)

    return render (request, 'customer_temp/Client_Reorder_dispatch.html', {'data':data, 'dispatch':dispatch })

def client_ticket(request):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id=user_id) 

    tickets = Robo_Ticket.objects.filter(client_id = data.client_id)
    all_tic = Robo_Ticket.objects.all()
    robots = Robot_Details.objects.filter(client_id = data.client_id)

    if request.method == 'POST':
        robot_id = request.POST.get('robot_id')
        robot_name = request.POST.get('robot_name')
        complaint_title = request.POST.get('complaint_title')
        complaint_description = request.POST.get('cmp_description')
        maintenance_date = request.POST.get('Maintenance_Date')

        # Autogenerate ticket number
        if all_tic.exists():
            last_ticket_num = all_tic.last().ticket_num
            pre = last_ticket_num[:-3]  
            suf = int(last_ticket_num[-3:])                        
            new_suf = suf + 1
            new_value = f"{pre}{new_suf:03}"
        else:           
            new_value = 'TCK001'  

        new_ticket = Robo_Ticket(
            client_id = data.client_id,
            client_name = data.client_name,
            robot_id = robot_id,
            robot_name =robot_name,
            ticket_num=new_value,
            complaint_title=complaint_title,
            cmp_description=complaint_description,
            ticket_date=timezone.now() + timedelta(hours=5, minutes=30),
            Maintenance_Date=maintenance_date,
            created_by=data.first_name,
            creation_date=timezone.now() + timedelta(hours=5, minutes=30),
            status='Open'
        )
        new_ticket.save()

        messages.success(request, 'Ticket Raised successfully.')
        return redirect('client_ticket')

    return render(request, 'customer_temp/client_ticket.html', {'data': data, 'tickets': tickets, 'robots':robots})

def edit_ticket(request,id):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id=user_id) 

    tickets = get_object_or_404(Robo_Ticket, id=id)
    robots = Robot_Details.objects.filter(client_id = data.client_id)

    if request.method == 'POST':
        tickets.complaint_title = request.POST.get('edit_complaint_title')
        tickets.cmp_description = request.POST.get('edit_cmp_description')
        tickets.Maintenance_Date = request.POST.get('edit_Maintenance_Date')
        tickets.ticket_date=timezone.now() + timedelta(hours=5, minutes=30)

        tickets.save()

        messages.success(request, "Ticket Has been Updated")
        return redirect ('client_ticket')
    
    return render(request, 'customer_temp/client_ticket.html', {'data': data, 'tickets': tickets, 'robots':robots})

def c_ticket_view(request,ticket_num):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id = user_id)

    tickets=Robo_Ticket.objects.get(ticket_num=ticket_num, client_id=data.client_id)
    client_dt=Client_Master.objects.get(client_id=tickets.client_id)
    
    return render (request, 'customer_temp/c_ticket_view.html', {'data':data,'tickets':tickets,'client_dt':client_dt,})

def close_ticket(request,ticket_num):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id = user_id)

    tickets=Robo_Ticket.objects.get(ticket_num=ticket_num, client_id=data.client_id)
    client_dt=Client_Master.objects.get(client_id=tickets.client_id)

    if request.method == 'POST':
        tickets.status = 'Closed'
        tickets.save()

        messages.success(request, "Ticket is Closed")
        return redirect ('client_ticket')
    
    return render (request, 'customer_temp/c_ticket_view.html', {'data':data,'tickets':tickets,'client_dt':client_dt,})


def received_view(request, ord_no):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id=user_id)

    order = get_object_or_404(manil_order, order_number=ord_no, client_id=data.client_id)
    ord_det = manil_order_details.objects.filter(process_num=ord_no)
    c_order = client_order.objects.get(order_number=order.order_number)
    c_ord_det = client_order_details.objects.filter(order_number=order.order_number)
    client_det = Client_Master.objects.get(client_id=order.client_id)
    mat_list = Material_Master.objects.all()
    dispatch = Despatch_Details.objects.get(order_number=ord_no)

    c_notification = Client_Notification.objects.get(order_number=ord_no)

    context = {
        'data': data,
        'order': order,
        'client_det': client_det,
        'ord_det': ord_det,
        'c_ord_det':c_ord_det,
        'mat_list': mat_list,
        'c_order': c_order,
        'dispatch': dispatch,
        'success_msg': None,
    }

    if request.method == "POST":
        # Update dispatch details
        dispatch.received_by = data.first_name
        dispatch.received_date = timezone.now() + timedelta(hours=5, minutes=30)
        dispatch.save()

        # Update order status
        order.status = 'Delivered'
        order.save()

        # Update client order status
        c_order.status = 'Delivered'
        c_order.save()

        c_notification.is_read = True
        c_notification.save()

        notification_title = "Raise Invoice"
        notification_message = f"We are pleased to inform you, the order with (Order No: {order.order_number}) was successfully Received on {timezone.now().strftime('%d-%m-%Y at %H:%M')}. By {data.first_name}, So please raise Invoice "


        # Create a new notification for the logged-in user
        m_notification = Inv_Notification(
            order_number = order.order_number,
            message=notification_message,
            title = notification_title
        )
        m_notification.save()

        # Prepare email notification
        order_details_rows = ""
        for index, detail in enumerate(c_ord_det, start=1):
            order_details_rows += f"""
            <tr>
                <td>{index}</td>
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
        <p>Dear Team,</p>
        <p>The following order has been successfully received:</p>

        <h3>Order Summary</h3>
        <p><strong>Order Number:</strong> {order.process_num}</p>
        <p><strong>Client Name:</strong> {client_det.client_name}</p>
        <p><strong>Received By:</strong> {data.first_name}</p>
        <p><strong>Received Date:</strong> {dispatch.received_date.strftime('%Y-%m-%d %H:%M:%S')}</p>

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
        client_email_objs = Client_emails.objects.filter(client_id=data.client_id)  
        for client_email_obj in client_email_objs:
            for i in range(1, 6):  # Loop through email1 to email5 fields
                email_field = f'email{i}'
                email = getattr(client_email_obj, email_field, None)
                if email:
                    client_emails.append(email)

        recipient_list = manil_emails + chaipoint_emails + client_emails

        # Send email
        email = EmailMessage(
            subject='Order Received Notification',
            body=email_body,
            from_email=settings.EMAIL_HOST_USER,
            to=recipient_list,
        )
        email.content_subtype = 'html'
        email.send(fail_silently=False)

        # Add success message
        messages.success(request, 'Order Received Successfully.')
        return redirect('order_table')

    return render(request, 'customer_temp/recieved_view.html', context)



def re_received_view(request, ord_no):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id=user_id)

    order = get_object_or_404(Re_manil_order, order_number=ord_no, client_id=data.client_id)
    ord_det = Re_manil_order_details.objects.filter(process_num=order.process_num)
    c_order = client_order.objects.get(order_number=order.order_number)
    c_ord_det = client_order_details.objects.filter(order_number=order.order_number)
    client_det = Client_Master.objects.get(client_id=order.client_id)
    mat_list = Material_Master.objects.all()
    dispatch = Re_Despatch_Details.objects.get(order_number=ord_no)

    cost_tbl = Costing_Table.objects.filter(client_id=data.client_id)

    c_notification = Client_Notification.objects.get(order_number=ord_no)

    new_values = {}
    grand_total = 0

    for i in ord_det:
        for j in mat_list:
            for k in cost_tbl:
                if i.material_name == j.material_name == k.material_name:
                    new_qty = int(i.qty / j.conversion_rate)
                    sub_total = new_qty * k.cost_per_unit
                    sub_total = round(sub_total + (sub_total * (i.gst_rate / 100)))

                    if i.material_name not in new_values:
                        new_values[i.material_name] = {}

                    new_values[i.material_name]['qty'] = new_qty
                    new_values[i.material_name]['sub_total'] = sub_total

    for key, value in new_values.items():
        grand_total += value['sub_total']

    grand_total_word = num2words(grand_total).title()

    context = {
        'data': data,
        'order': order,
        'client_det': client_det,
        'ord_det': ord_det,
        'c_ord_det': c_ord_det,
        'mat_list': mat_list,
        'c_order': c_order,
        'dispatch': dispatch,
        'success_msg': None,
        'grand_total_word': grand_total_word,
        'cost_tbl': cost_tbl,
        'new_values': new_values,
        'grand_total': grand_total
    }

    if request.method == "POST":
        dispatch.received_by = data.first_name
        dispatch.received_date = timezone.now() + timedelta(hours=5, minutes=30)
        dispatch.save()

        order.status = 'Delivered'
        order.save()

        c_order.status = 'Delivered'
        c_order.save()

        c_notification.is_read = True
        c_notification.save()

        notification_title = "Order Received Successfully"
        notification_message = (
            f"The order with Order Number {order.order_number} was successfully received on "
            f"{timezone.now().strftime('%d-%m-%Y at %H:%M')} by {data.first_name}. "
            f"Please proceed to raise the invoice."
        )

        m_notification = Inv_Notification(
            order_number=order.order_number,
            message=notification_message,
            title=notification_title
        )
        m_notification.save()

        order_details_rows = ""
        for index, detail in enumerate(c_ord_det, start=1):
            order_details_rows += f"""
            <tr>
                <td>{index}</td>
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
        <p>Dear Team,</p>
        <p>The following order has been successfully received:</p>

        <h3>Order Summary</h3>
        <p><strong>Order Number:</strong> {order.process_num}</p>
        <p><strong>Client Name:</strong> {client_det.client_name}</p>
        <p><strong>Received By:</strong> {data.first_name}</p>
        <p><strong>Received Date:</strong> {dispatch.received_date.strftime('%Y-%m-%d %H:%M:%S')}</p>

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

        <p><strong>Total Amount:</strong> {grand_total}</p>
        <p><strong>Amount in Words:</strong> {grand_total_word}</p>
        <p>Thank you!</p>
        """

        manil_email_obj = Manil_emails.objects.first()
        manil_emails = [
            manil_email_obj.email1,
            manil_email_obj.email2,
            manil_email_obj.email3,
            manil_email_obj.email4,
            manil_email_obj.email5
        ] if manil_email_obj else []

        chaipoint_email_obj = Chaipoint_emails.objects.first()
        chaipoint_emails = [
            chaipoint_email_obj.email1,
            chaipoint_email_obj.email2,
            chaipoint_email_obj.email3,
            chaipoint_email_obj.email4,
            chaipoint_email_obj.email5
        ] if chaipoint_email_obj else []

        client_emails = []
        client_email_objs = Client_emails.objects.filter(client_id=data.client_id)
        for client_email_obj in client_email_objs:
            for i in range(1, 6):
                email_field = f'email{i}'
                email = getattr(client_email_obj, email_field, None)
                if email:
                    client_emails.append(email)

        recipient_list = manil_emails + chaipoint_emails + client_emails

        email = EmailMessage(
            subject='Order Received Notification',
            body=email_body,
            from_email=settings.EMAIL_HOST_USER,
            to=recipient_list,
        )
        email.content_subtype = 'html'
        email.send(fail_silently=False)

        messages.success(request, 'Order Received Successfully.')
        return redirect('order_table')

    return render(request, 'customer_temp/re_recieved_view.html', context)



def remarks_view(request, ord_no):
    # Fetch user and order details
    user_id = request.session.get('user_id')
    data = get_object_or_404(Client_user, user_id=user_id)

    order = get_object_or_404(manil_order, order_number=ord_no)

    c_order = client_order.objects.get(order_number=order.order_number)

    c_notification = Client_Notification.objects.get(order_number=ord_no)

    # Fetch order details (assuming there's a related model or data source)
    c_ord_det = client_order_details.objects.filter(order_number=ord_no)  # Replace `client_order_details` with your model name for order details.

    # Generate a new ticket number
    tickets = Order_Tickets.objects.filter(client_id=data.client_id)
    all_tck = Order_Tickets.objects.all()

    if all_tck:
        last_ticket_num = all_tck.last().ticket_num
        pre = last_ticket_num[:-3]
        suf = int(last_ticket_num[-3:])
        new_ticket_num = f"{pre}{suf + 1:03}"
    else:
        new_ticket_num = 'RMK001'
    
    print('new_ticket_num', new_ticket_num)

    if request.method == "POST":
        # Save remarks in Order_Tickets
        order_remark = Order_Tickets(
            process_num=order.process_num,
            order_number=ord_no,
            client_id=data.client_id,
            client_name=data.client_name,
            ticket_num=new_ticket_num,
            ticket_date=timezone.now() + timedelta(hours=5, minutes=30),
            remarks_title=request.POST.get("remarks_title"),
            remarks=request.POST.get("remarks"),
            remarked_by=data.first_name,
            remarked_date=timezone.now() + timedelta(hours=5, minutes=30),
            remarks_type=request.POST.get("remarks_type"),
        )
        order_remark.save()

        # Save order details for each material
        for i in c_ord_det:             
            received_qty_key = f"received_quantity_{i.id}"
            received_qty = request.POST.get(received_qty_key, 0) 
            
            Order_Tickets_details.objects.create(
                order_number=ord_no,
                material_name=i.material_name,
                order_qty=i.qty,
                received_qty=received_qty,
                uom = i.uom
            )

        # Save attached images
        images = request.FILES.getlist("image")
        for image in images:
            Remarkes_images.objects.create(order_number=ord_no, image=image)

        # Update statuses
        order.status = 'Remarked'
        order.save()

        c_order.status = 'Remarked'
        c_order.save()

        c_notification.is_read = True
        c_notification.save()

        notification_title = "Order Remark"
        notification_message = (
            f"The order with Order Number {order.order_number} was received on Damaged State "
            f"{timezone.now().strftime('%d-%m-%Y at %H:%M')} by {data.first_name}. "
            f"Please look into it and make a order replacement."
        )

        m_notification = Inv_Notification(
            order_number=order.order_number,
            message=notification_message,
            title=notification_title
        )
        m_notification.save()

        # Success message and redirect
        messages.success(request, 'Remark and images saved successfully.')
        return redirect("c_order_remarks")

    return render(request, 'customer_temp/recieved_view.html', {
        'data': data,
        'order': order,
        'tickets': tickets,
        'c_order': c_order,
        'c_ord_det': c_ord_det,
    })


def c_order_remarks(request):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id=user_id)

    tickets = Order_Tickets.objects.filter(
        client_id = data.client_id,
        remarks__isnull=False,
        remarks_title__isnull=False,
        remarked_by__isnull=False,
        remarked_date__isnull=False
    )

    return render(request, 'customer_temp/remarked_order.html', {'data': data, 'tickets': tickets})

def c_order_remarks_view(request, ord_no):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id=user_id)

    tickets = get_object_or_404( Order_Tickets , order_number=ord_no, client_id=data.client_id)

    images = Remarkes_images.objects.filter(order_number=ord_no)

    return render(request, 'customer_temp/remarked_order_view.html', {'data': data,'tickets': tickets,'images': images })

def invoice_table (request):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id = user_id)

    invoice = M_client_invoice.objects.filter(client_id = data.client_id)


    return render (request, 'customer_temp/invoice_table.html', {'data':data, 'invoice':invoice})

def client_invoice_view(request, ord_no):    
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id = user_id)

    manil_det = Manil_db.objects.first()

    order = client_order.objects.get(order_number = ord_no)

    client_det = Client_Master.objects.get(client_id = order.client_id)

    ord_det = client_order_details.objects.filter(order_number = ord_no)

    mat_list = Material_Master.objects.all()
    
    dispatch = Despatch_Details.objects.all()

    invoice = M_client_invoice.objects.get(order_number=order.order_number)


    context = {'data':data, 'order':order, 'client_det':client_det, 'ord_det':ord_det, 'mat_list':mat_list, 'dispatch':dispatch, 'manil_det':manil_det, 'invoice':invoice }
    
    return render (request, 'customer_temp/client_invoice_view.html', context)


from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import black, white, grey
from io import BytesIO
from django.http import HttpResponse
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
import os 
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Flowable,PageBreak
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Image
from reportlab.platypus import Flowable
from reportlab.lib.pagesizes import A4
import logging
from reportlab.pdfgen import canvas

def download_invoice(request, ord_no):
    # Fetch data
    user_id = request.session.get('user_id')
    try:
        data = Client_user.objects.get(user_id=user_id)
        manil_det = Manil_db.objects.first()
        order = client_order.objects.get(order_number=ord_no)
        client_det = Client_Master.objects.get(client_id=order.client_id)
        ord_det = client_order_details.objects.filter(order_number=ord_no)
        invoice = M_client_invoice.objects.get(order_number=ord_no)
    except Exception as e:
        return HttpResponse(str(e), status=404)
    
    c_inv_notification = Client_Inv_Notification .objects.get(order_number=ord_no)
    
    if request.method == "POST":
        c_inv_notification.is_read = True
        c_inv_notification.save()

    # Initialize the response object for PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{ord_no}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=64, bottomMargin=60)
    styles = getSampleStyleSheet()
    flowables = []

    # Attach manil_det to doc object so it can be accessed in the header
    doc.manil_det = manil_det  # Store manil_det in the doc object

    # Header content for the first page
    def first_page_header(canvas, doc):
        # Access manil_det from the doc object
        manil_det = doc.manil_det
        
        canvas.saveState()  # Save the current state

        logo_path = Path("media/invoice/manil.jpg") 
        img_width = 240 
        img_height = 45
        canvas.drawImage(logo_path, (A4[0]-img_width)/2, A4[1] - 60, width=img_width, height=img_height)

        canvas.setFont("Helvetica-Bold", 14)
        canvas.setFillColor(colors.black)
        canvas.drawCentredString(300, 750, "TAX INVOICE")
        
        canvas.setLineWidth(1)
        canvas.line(25, 740, 570, 740)
        
        normal_style = styles["Normal"]
        normal_style.fontName = "Helvetica"
        normal_style.fontSize = 10
        
        company_details = (f"{manil_det.company_name}<br/>{manil_det.billing_address}<br/>"
            f"{manil_det.billing_city}, {manil_det.billing_state}-{manil_det.billing_pin}<br/>"
            f"GSTIN - {manil_det.billing_gst_number}<br/>"
            f"MSME Registration No: {manil_det.msme_number}"
        )
        
        company_paragraph = Paragraph(company_details, normal_style)
        company_paragraph.wrapOn(canvas, 250, 300)
        company_paragraph.drawOn(canvas, 30, 665)

        # Vertical Divider
        canvas.line(290, 740, 290, 590) 

        # Invoice Details
        invoice_details = (
            f"Invoice Number: {invoice.invoice_num}<br/>"
            f"Invoice Date: {invoice.invoice_date.strftime('%d-%m-%Y')}"
        )   
        invoice_paragraph = Paragraph(invoice_details, normal_style)
        invoice_paragraph.wrapOn(canvas, 250, 200)  # Wrap within 250 points width
        invoice_paragraph.drawOn(canvas, 300, 705)

        canvas.setLineWidth(1)
        canvas.line(25, 655, 570, 655)

        # Billing Details
        billing_details = (
            f"<b>BILL TO</b>:<br/>"
            f"{client_det.billing_address}<br/>{client_det.billing_city},"
            f"{client_det.billing_state}-{client_det.billing_pin}<br/>"
            f"GSTIN: {client_det.billing_gst_number}"
        )        
        billing_paragraph = Paragraph(billing_details, normal_style)
        billing_paragraph.wrapOn(canvas, 250, 200)  # Wrap within 250 points width
        billing_paragraph.drawOn(canvas, 30, 605)

        # Shipping Details
        shipping_details = (
            f"<b>SHIP TO</b>:<br/>"
            f"{client_det.shipping_address}<br/>{client_det.shipping_city},"
            f"{client_det.shipping_state}-{client_det.shipping_pin}<br/>"
            f"GSTIN: {client_det.shipping_gst_number}"
        )        
        shipping_paragraph = Paragraph(shipping_details, normal_style)
        shipping_paragraph.wrapOn(canvas, 250, 200)  # Wrap within 250 points width
        shipping_paragraph.drawOn(canvas, 300, 605)

        canvas.setLineWidth(1)
        canvas.line(25, 590, 570, 590)

        # Po_details
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(black)
        canvas.drawString(30, 570, f'Ref: PO Authority: {order.po_authority} and PO Date: {order.po_authority_date}')

        # canvas.setLineWidth(0.5)
        # canvas.line(30, 560, 570, 560)

        # Draw the page border
        canvas.setStrokeColor(colors.black)
        canvas.setLineWidth(1)
        canvas.rect(25, 50, A4[0] - 50, A4[1] - 120)

        canvas.restoreState()  # Restore the state after drawing

    def later_pages_header(canvas, doc):
        canvas.saveState()  # Ensure state is saved
        logo_path = Path("media/invoice/manil.jpg")
        img_width = 240
        img_height = 45
        canvas.drawImage(logo_path, (A4[0] - img_width) / 2, A4[1] - 60, width=img_width, height=img_height)

        # canvas.setLineWidth(0.5)
        # canvas.line(30, 770, 570, 770)

        # Draw the page border for later pages
        canvas.setStrokeColor(colors.black)
        canvas.setLineWidth(1)
        canvas.rect(25, 50, A4[0] - 50, A4[1] - 120)
        # Add page numbers for later pages if needed
        canvas.restoreState()

    # Add a flag to identify if the shipping state is Karnataka
    is_karnataka = client_det.shipping_state.casefold() == 'karnataka'.casefold()

    # Define column widths and headers based on the shipping state
    if is_karnataka:
        table_header = [
            ['Sr No', 'Particular', 'Nos', 'Unit Price', 'Base', 'GST %', 'HSN Code', 'IGST', 'Total Amount(Rs.)']
        ]
        col_widths = [30, 85, 40, 60, 60, 50, 70, 50, 100]  # Adjusted column widths for Karnataka
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Header alignment
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # Body alignment for numbers
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('FONTSIZE', (0, 0), (-1, 0), 10),  # Header font size
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Body background
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Table grid
            ('SPAN', (0, -1), (3, -1)),  # Merge the first four cells in the "Total" row
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),  # Make merged cell text bold
            ('ALIGN', (0, -1), (0, -1), 'CENTER'),  # Center-align the merged cell text
            ('TEXTCOLOR', (0, -1), (0, -1), colors.black),  # Set text color for the merged cell
        ])
    else:
        table_header = [
            ['Sr No', 'Particular', 'Nos', 'Unit Price', 'Base', 'GST %', 'HSN Code', 'CGST', 'SGST', 'Total Amount(Rs.)']
        ]
        col_widths = [30, 75, 35, 55, 55, 45, 60, 45, 45, 100]  # Adjusted column widths for other states
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Header alignment
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # Body alignment for numbers
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('FONTSIZE', (0, 0), (-1, 0), 10),  # Header font size
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Body background
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Table grid
            ('SPAN', (0, -1), (3, -1)),  # Merge the first four cells in the "Total" row
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),  # Make merged cell text bold
            ('ALIGN', (0, -1), (0, -1), 'CENTER'),  # Center-align the merged cell text
            ('TEXTCOLOR', (0, -1), (0, -1), colors.black),  # Set text color for the merged cell
        ])

    # Continue table logic for row data
    data = table_header.copy()
    grand_total_base = grand_total_cgst = grand_total_sgst = grand_total = grand_total_igst = 0.00

    for i, item in enumerate(ord_det):
        qty = item.qty
        unit_price = item.base_price
        subtotal = qty * unit_price
        gst_rate = item.gst_rate
        hsn_code = item.hsn_code

        if is_karnataka:
            igst_amount = subtotal * (gst_rate / 100)
            total_amount = subtotal + igst_amount
            data.append([
                str(i + 1), item.material_name, str(qty), f"{unit_price:.2f}",
                f"{subtotal:.2f}", f"{gst_rate}%", hsn_code,
                f"{igst_amount:.2f}", f"{total_amount:.2f}"
            ])
            grand_total += total_amount
            grand_total_igst += igst_amount
            grand_total_base += subtotal
        else:
            cgst = sgst = gst_rate / 2
            cgst_amount = subtotal * (cgst / 100)
            sgst_amount = subtotal * (sgst / 100)
            total_amount = subtotal + cgst_amount + sgst_amount
            data.append([
                str(i + 1), item.material_name, str(qty), f"{unit_price:.2f}",
                f"{subtotal:.2f}", f"{gst_rate}%", hsn_code,
                f"{cgst_amount:.2f}", f"{sgst_amount:.2f}", f"{total_amount:.2f}"
            ])
            grand_total += total_amount
            grand_total_base += subtotal
            grand_total_cgst += cgst_amount
            grand_total_sgst += sgst_amount

    # Add total row
    if is_karnataka:
        data.append(['Total', '', '', '', f"{grand_total_base:.2f}", '', '', f"{grand_total_igst:.2f}", f"{grand_total:.2f}"])
    else:
        data.append(['Total', '', '', '', f"{grand_total_base:.2f}", '', '', f"{grand_total_cgst:.2f}", f"{grand_total_sgst:.2f}", f"{grand_total:.2f}"])

    # Add spacer
    first_page_spacer = Spacer(1, 220)  # Adjust spacer height as needed
    flowables.append(first_page_spacer)

    # Build the table
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(table_style)
    flowables.append(table)
    

    # Adding additional information after the table
    amountwords_details = Paragraph(
        f"Total amount in words: <b>{order.ammount_words}</b>", styles['Normal']
    )
    amountwords_spacer = Spacer(1, 0.2 * inch)  # Spacer for some padding
    flowables.append(amountwords_spacer)
    flowables.append(amountwords_details)

    # Line below amountwords_details
    flowables.append(Spacer(1, -0.1 * inch))
    flowables.append(
        Table([[""]], colWidths=[545], style=[("LINEBELOW", (0, 0), (-1, -1), 1, colors.black)])
    )
    
    # Signature Section
    seal_image_path = Path("media/invoice/image.png")
    signature_image_path = Path("media/invoice/sign.jpg")

    
    # Right side (Seal and Signature Section)
    seal_and_signature_table = Table([
        # "For MANIL ADVISORS" text
        [Paragraph("<b>For MANIL ADVISORS</b>", styles['Normal'])],
        # Signature image and Seal
        [Image(str(signature_image_path), width=100, height=50),[Image(str(seal_image_path), width=90, height=70)]],
        # "Authorised Signatory" text directly below the signature image
        [Paragraph("Authorised Signatory", styles['Normal'])],
        # Seal image as a separate row
        # [Image(str(seal_image_path), width=90, height=90)],
    ], colWidths=[150], style=[
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align everything
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Top-align all elements
        ('TOPPADDING', (0, 0), (-2, -2), 0),  # Remove top padding
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),  # Remove bottom padding
        ('LEFTPADDING', (0, 0), (-1, -1), 0),  # Remove left padding
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),  # Remove right padding
    ])


    # Account and Signature Layout
    account_and_signature_data = [
        [
            # Left side (Account Details)
            Paragraph(
                "All Cheques/Demand Drafts/Wire transfers should be made favouring <br/>"
                "MANIL ADVISORS <br/>"
                "Account Number:  XXXXXXXXXXXX <br/>"
                "IFSC Code: XXXXXXXXXXXX <br/>"
                "HDFC Bank Ltd <br/> Malleswaram Branch",
                styles['Normal']
            ),
            # Right side (Seal and Signature Section)
            seal_and_signature_table
        ]
    ]

    # Create the layout using a table with two columns
    account_and_signature_table = Table(account_and_signature_data, colWidths=[250, 300], style=[
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # Align left for account details
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),  # Center-align seal and signature section
        ('VALIGN', (0, 0), (0, -1), 'TOP'),  # Top-align account details
        ('VALIGN', (1, 0), (1, -1), 'TOP'),  # Top-align signature section
        ('LINEBEFORE', (1, 0), (2, -1), 1, colors.black),  # Add vertical line before the second column
    ])

    # Add a spacer before the table
    # flowables.append(Spacer(1, 0.5 * inch))
    flowables.append(account_and_signature_table)

    flowables.append(Spacer(1, -0.25 * inch))
    flowables.append(
        Table([[""]], colWidths=[545], style=[("LINEBELOW", (0, 0), (-1, -1), 1, colors.black)])
    )

    try:
        # Now doc will have access to manil_det
        doc.build(flowables, onFirstPage=first_page_header, onLaterPages=later_pages_header)
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return HttpResponse(f"Error generating the PDF: {str(e)}", status=500)

    return response



def delete_user(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Client_user, user_id=user_id)
    
    client_user = get_object_or_404(Client_user, id=id)
    client_user.delete()

    messages.success(request, 'Client user is Deletd Successfully')
    return redirect('add_user')

def delete_c_order(request, order_number):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Client_user, user_id=user_id)
    
    c_order = get_object_or_404(client_order, order_number=order_number)
    c_order.delete()

    c_order_details = client_order_details.objects.filter(order_number=order_number)
    c_order_details.delete()

    messages.success(request, 'Client Order is Deleted Successfully')
    return redirect('order_table')

def delete_c_dispatch(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Client_user, user_id=user_id)
    
    m_dispatch = get_object_or_404(Despatch_Details, id=id)
    m_dispatch.delete()

    m_order = get_object_or_404(manil_order, process_num=m_dispatch.process_num)
    m_order.status = "Order Placed"
    m_order.save()

    c_order = get_object_or_404(client_order, order_number=m_dispatch.order_number)
    c_order.status = "In Progress"
    c_order.save()

    messages.success(request, 'Dispatch details are Deleted Successfully')
    return redirect('Client_dispatch')

def delete_c_invoice(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Client_user, user_id=user_id)
    
    invoice = get_object_or_404( M_client_invoice, id=id)
    invoice.delete()

    messages.success(request, 'Invoice is Deleted Successfully')
    return redirect('invoice_table')

def delete_c_order_remark(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Client_user, user_id=user_id)
    
    order_remark = get_object_or_404( Order_Tickets, id=id)
    order_remark.delete()

    messages.success(request, 'Order Remark is Deleted Successfully')
    return redirect('c_order_remarks')


def delete_c_robot_ticket(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Client_user, user_id=user_id)
    
    robo_ticket = get_object_or_404( Robo_Ticket, id=id)
    robo_ticket.delete()

    messages.success(request, 'Robot Ticket is Deleted Successfully')
    return redirect('client_ticket')