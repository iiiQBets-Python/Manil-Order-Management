from Manil_Management.imports import *
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import EmailMessage

from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from io import BytesIO



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
    
    return render(request, 'customer_temp/client_emails.html', {'data': data, 'emails': emails})


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
                <td>{hsn_code}</td>
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

    dispatch = Despatch_Details.objects.filter(client_id = data.client_id)

    return render (request, 'customer_temp/Client_dispatch.html', {'data':data, 'dispatch':dispatch})

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

    order = get_object_or_404(manil_order, process_num=ord_no, client_id=data.client_id)
    ord_det = manil_order_details.objects.filter(process_num=ord_no)
    c_order = client_order.objects.get(order_number=order.order_number)
    client_det = Client_Master.objects.get(client_id=order.client_id)
    mat_list = Material_Master.objects.all()
    dispatch = Despatch_Details.objects.get(process_num=ord_no)

    context = {
        'data': data,
        'order': order,
        'client_det': client_det,
        'ord_det': ord_det,
        'mat_list': mat_list,
        'c_order': c_order,
        'dispatch': dispatch,
        'success_msg': None  
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

        # Prepare email notification
        order_details_rows = ""
        for index, detail in enumerate(ord_det, start=1):
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


def remarks_view(request, ord_no):
    # Fetch user and order details
    user_id = request.session.get('user_id')
    data = get_object_or_404(Client_user, user_id=user_id)  

    order = get_object_or_404(manil_order, process_num=ord_no)  
    
    c_order = client_order.objects.get(order_number=order.order_number)

    # Generate a new ticket number
    tickets = Order_Tickets.objects.filter(client_id = data.client_id)
    all_tck = Order_Tickets.objects.all()

    if all_tck:
        last_ticket_num = all_tck.last().ticket_num
        pre = last_ticket_num[:-3]
        suf = int(last_ticket_num[-3:])
        new_ticket_num = f"{pre}{suf + 1:03}"
    else:
        new_ticket_num = 'RMK001'

    if request.method == "POST":
        order_remark = Order_Tickets(
            process_num=ord_no,
            order_number= order.order_number,
            client_id=data.client_id,
            client_name=data.client_name,
            ticket_num=new_ticket_num,
            ticket_date=timezone.now() + timedelta(hours=5, minutes=30),
            remarks_title=request.POST.get("remarks_title"),
            remarks=request.POST.get("remarks"),
            remarked_by=data.first_name,
            remarked_date=timezone.now() + timedelta(hours=5, minutes=30),
        )
        order_remark.save()

        # Save attached images
        images = request.FILES.getlist("image")
        for image in images:
            Remarkes_images.objects.create(process_num=ord_no, image=image)
        
        order.status = 'Remarked'
        order.save()

        c_order.status = 'Remarked'
        c_order.save()

        # Success message and render the view
        messages.success(request, 'Remark and images saved successfully.')
        return redirect("c_order_remarks")
       
    return render( request,'customer_temp/recieved_view.html',{'data': data,'order': order, 'tickets':tickets, 'c_order':c_order} )

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

    tickets = get_object_or_404( Order_Tickets , process_num=ord_no, client_id=data.client_id)

    images = Remarkes_images.objects.filter(process_num=ord_no)

    return render(request, 'customer_temp/remarked_order_view.html', {'data': data,'tickets': tickets,'images': images })

def invoice_table (request):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id = user_id)

    invoice = M_client_invoice.objects.filter(client_id = data.client_id)


    return render (request, 'customer_temp/invoice_table.html', {'data':data, 'invoice':invoice})

def client_invoice_view(request, ord_no):    
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id = user_id)

    manil_det = Manil_db.objects.all()

    order = client_order.objects.get(order_number = ord_no)

    client_det = Client_Master.objects.get(client_id = order.client_id)

    ord_det = client_order_details.objects.filter(order_number = ord_no)

    mat_list = Material_Master.objects.all()
    
    dispatch = Despatch_Details.objects.all()

    invoice = M_client_invoice.objects.get(order_number=order.order_number)


    context = {'data':data, 'order':order, 'client_det':client_det, 'ord_det':ord_det, 'mat_list':mat_list, 'dispatch':dispatch, 'manil_det':manil_det, 'invoice':invoice }
    
    return render (request, 'customer_temp/client_invoice_view.html', context)

from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
from django.conf import settings

def download_invoice(request, ord_no):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id=user_id)

    
    manil_det = Manil_db.objects.all()
    order = client_order.objects.get(order_number=ord_no)
    client_det = Client_Master.objects.get(client_id=order.client_id)
    ord_det = client_order_details.objects.filter(order_number=ord_no)
    mat_list = Material_Master.objects.all()
    dispatch = Despatch_Details.objects.all()
    invoice = M_client_invoice.objects.get(order_number=order.order_number)

    context = {
        'data': data,
        'order': order,
        'client_det': client_det,
        'ord_det': ord_det,
        'mat_list': mat_list,
        'dispatch': dispatch,
        'manil_det': manil_det,
        'invoice': invoice,
    }

    rendered_html = render_to_string('customer_temp/invoice_pdf.html', context)
    result = BytesIO()

    pdf = pisa.CreatePDF(BytesIO(rendered_html.encode("UTF-8")), dest=result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{ord_no}.pdf"'
        return response
    else:
        return HttpResponse('We had some errors with the PDF generation', status=500)



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