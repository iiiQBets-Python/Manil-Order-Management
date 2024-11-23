from Manil_Management.imports import *
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from io import BytesIO



def Client_dashboard(request):    
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id = user_id)   

    
    return render(request, 'customer_temp/Client_dashboard.html', {'data':data,  "range_20": range(20)})

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

        com_user.upadated_date = timezone.now() + timedelta(hours=5, minutes=30)
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

        messages.success(request, 'Your order has been Placed.')
        return redirect('order_table')

    return render (request, 'customer_temp/order_table.html', context)




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


def received_view(request, ord_no):
    user_id = request.session.get('user_id')
    data = Client_user.objects.get(user_id=user_id)

    order = get_object_or_404(manil_order, process_num=ord_no)
    ord_det = manil_order_details.objects.filter(process_num=ord_no)
    c_order = client_order.objects.get(order_number=order.order_number)
    client_det = Client_Master.objects.get(client_id=order.client_id)
    mat_list = Material_Master.objects.all()
    dispatch = Despatch_Details.objects.get(process_num=ord_no)

    existing_tickets = Order_Tickets.objects.filter(client_id=order.client_id).exists()

    context = {
        'data': data,
        'order': order,
        'client_det': client_det,
        'ord_det': ord_det,
        'mat_list': mat_list,
        'c_order': c_order,
        'dispatch': dispatch,
        'hide_dropdown':  existing_tickets or order.status == "Delivered",
        'success_msg': None  
    }

    if request.method == "POST":
        dispatch.received_by = data.first_name
        dispatch.received_date = timezone.now() + timedelta(hours=5, minutes=30)
        dispatch.save()

        order.status = 'Delivered'
        order.save()

        c_order.status = 'Delivered'
        c_order.save()

        messages.success(request, 'Order Received Successfully.')
        return redirect('order_table')

    return render(request, 'customer_temp/recieved_view.html', context)


def remarks_view(request, ord_no):
    # Fetch user and order details
    user_id = request.session.get('user_id')
    data = get_object_or_404(Client_user, user_id=user_id)  # Fetch client user or return 404
    order = get_object_or_404(manil_order, process_num=ord_no)  # Fetch order or return 404

    # Generate a new ticket number
    last_ticket = Order_Tickets.objects.filter(process_num=ord_no).order_by('ticket_num').last()
    if last_ticket:
        last_ticket_num = last_ticket.ticket_num
        pre = last_ticket_num[:-3]
        suf = int(last_ticket_num[-3:])
        new_ticket_num = f"{pre}{suf + 1:03}"
    else:
        new_ticket_num = 'ORTCK001'

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

        # Success message and render the view
        messages.success(request, 'Remark and images saved successfully.')
        return redirect("order_table")
       
    return render( request,'customer_temp/recieved_view.html',{'data': data,'order': order,} )

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


