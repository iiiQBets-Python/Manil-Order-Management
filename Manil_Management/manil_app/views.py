
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from Manil_Management.imports import *
from django.core.mail import EmailMessage
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import EmailMessage
from xhtml2pdf import pisa
from io import BytesIO
from django.shortcuts import render, redirect
from django.conf import settings
from num2words import num2words
from django.core.mail import EmailMessage
from django.conf import settings


def base(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)

    order_placed_count = client_order.objects.filter(status="Order Placed").count()

    # Fetch unread notifications
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')
    
    # Count the unread notifications
    unread_count = notifications.count()

    return render(request, 'manil_temp/base.html', {
        'data': data,
        'order_placed_count': order_placed_count,
        'unread_count': unread_count,
        'notifications': notifications,  
    })




def login_page(request):
    if request.method == 'POST':
        clientid = request.POST.get('clientid')
        password = request.POST.get('password')

        try:
            m_user = Manil_User.objects.get(user_id = clientid)
        except:
            m_user = None
        
        try:
            c_user = Client_user.objects.get(user_id = clientid)
        except:
            c_user = None
        
        try:
            p_user = chai_point_user.objects.get(user_id = clientid)
        except:
            p_user = None

        if m_user:
            if check_password(password, m_user.password):
                request.session['user_id'] = m_user.user_id
                messages.success(request, 'Login Successful!')
                return redirect('manil_dashboard')                          
        if c_user:
            if check_password(password, c_user.password):
                request.session['user_id'] = c_user.user_id
                messages.success(request, 'Login Successful!') 
                return redirect('Client_dashboard')       
        if p_user:
            if check_password(password, p_user.password):
                request.session['user_id'] = p_user.user_id
                messages.success(request, 'Login Successful!')
                return redirect('cp_dashboard')  
                
        messages.error(request, 'Please enter valid credentials')
        return render(request, 'Base/login.html')        
    return render(request, 'Base/login.html')

@csrf_exempt
def log_out(request):
    user_id = request.session.get('user_id')
    if user_id:
        request.session.clear()
    return redirect('login_page')

from datetime import datetime, timedelta    

def manil_dashboard(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)

    # Orders
    c_orders = client_order.objects.all()
    total_orders = c_orders.count()
    processed_orders = c_orders.filter(status='Dispatched').count()
    pending_orders = c_orders.filter(status='Order Placed').count()
    delivered_orders = c_orders.filter(status='Delivered').count()
    remarked_orders = c_orders.filter(status='Remarked').count()

    # Tickets
    m_tickets = Robo_Ticket.objects.all()
    total_tickets = m_tickets.count()
    solved_tickets = m_tickets.filter(status='Closed').count()
    pending_tickets = m_tickets.filter(status='Open').count()

    # Filter Orders
    filter_type = request.GET.get('filter', 'all')
    today = datetime.now()
    if filter_type == 'day':
        filtered_orders = client_order.objects.filter(order_date__date=today.date())
    elif filter_type == 'week':
        start_of_week = today - timedelta(days=today.weekday())
        filtered_orders = client_order.objects.filter(order_date__date__gte=start_of_week.date())
    elif filter_type == 'month':
        filtered_orders = client_order.objects.filter(order_date__month=today.month, order_date__year=today.year)
    else:
        filtered_orders = client_order.objects.all()

    # Filter Tickets
    ticket_filter_type = request.GET.get('ticket_filter', 'all')
    if ticket_filter_type == 'day':
        filtered_tickets = Robo_Ticket.objects.filter(creation_date__date=today.date())
    elif ticket_filter_type == 'week':
        start_of_week = today - timedelta(days=today.weekday())
        filtered_tickets = Robo_Ticket.objects.filter(creation_date__date__gte=start_of_week.date())
    elif ticket_filter_type == 'month':
        filtered_tickets = Robo_Ticket.objects.filter(creation_date__month=today.month, creation_date__year=today.year)
    else:
        filtered_tickets = Robo_Ticket.objects.all()

    # Ticket Counts
    filtered_ticket_count = filtered_tickets.count()

    # Order Counts
    filtered_order_count = filtered_orders.count()
   

    # All Orders and Tickets
    all_orders = client_order.objects.all()
    all_tickets = Robo_Ticket.objects.all()

    context = {
        'filtered_orders': filtered_orders,
        'all_orders': all_orders,
        'filtered_order_count': filtered_order_count,
        'filtered_tickets': filtered_tickets,
        'all_tickets': all_tickets,
        'filtered_ticket_count': filtered_ticket_count,
        'data': data,
        'c_orders': c_orders,
        'm_tickets': m_tickets,
        'total_orders': total_orders,
        'processed_orders': processed_orders,
        'pending_orders': pending_orders,
        'delivered_orders':delivered_orders,
        'remarked_orders': remarked_orders,
        'total_tickets': total_tickets,
        'solved_tickets': solved_tickets,
        'pending_tickets': pending_tickets,
    }

    return render(request, 'manil_temp/manil_dashboard.html', context)


def forgot_password(request):
    return render(request, 'Base/forgot_password.html')

def manil_master(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)
    C_data = Manil_db.objects.first()
     
    if not C_data:
        C_data = Manil_db() 
    
    if request.method == 'POST':        
        
        if 'company_name' in request.POST:
            # Company Details Form (form1)
            C_data.company_name = request.POST.get('company_name')
            C_data.date_of_incorporation = parse_date(request.POST.get('date_of_incorporation'))
            C_data.pan = request.POST.get('pan')
            C_data.fssai_number = request.POST.get('fssai_number')
            C_data.msme_number = request.POST.get('msme_number')

        if 'bank_name' in request.POST:
            # Bank Details Form (form2)
            C_data.bank_name = request.POST.get('bank_name')
            C_data.branch = request.POST.get('branch')
            C_data.ifsc = request.POST.get('ifsc')
            C_data.account_number = request.POST.get('account_number')
            C_data.bank_address = request.POST.get('bank_address')

        if 'billing_gst_number' in request.POST:
            # Billing Details Form (form3)
            C_data.billing_gst_number = request.POST.get('billing_gst_number') 
            C_data.billing_address = request.POST.get('billing_address')
            C_data.billing_city = request.POST.get('billing_city')
            C_data.billing_state = request.POST.get('billing_state')
            C_data.billing_pin = request.POST.get('billing_pin') or None

        if 'shipping_gst_number' in request.POST:
            # Shipping Details Form (form4)
            C_data.shipping_gst_number = request.POST.get('shipping_gst_number')
            C_data.shipping_address = request.POST.get('shipping_address')
            C_data.shipping_city = request.POST.get('shipping_city')
            C_data.shipping_state = request.POST.get('shipping_state')
            C_data.shipping_pin = request.POST.get('shipping_pin') or None
        
        C_data.save()
    
    
    return render (request, 'manil_temp/manil_master.html', {'data':data, 'C_data':C_data})


def manil_emails(request):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)
    clients = Client_Master.objects.all()

    # Initialize Manil Emails and Chaipoint Emails
    m_emails = Manil_emails.objects.first() or Manil_emails()
    cp_emails = Chaipoint_emails.objects.first() or Chaipoint_emails()

    selected_client_id = request.POST.get('client_id')
    
    # Fetch all client emails for the selected client_id
    c_emails = Client_emails.objects.all()

    selected_client_id = request.GET.get('client_id', None)

    if selected_client_id:
        c_emails = Client_emails.objects.filter(client_id=selected_client_id)
        c_email_data_exists = c_emails.exists()
    else:
        c_emails = Client_emails.objects.none()  # Or default data
        c_email_data_exists = False

    m_email_data_exists = any([m_emails.username1, m_emails.email1,
                               m_emails.username2, m_emails.email2,
                               m_emails.username3, m_emails.email3,
                               m_emails.username4, m_emails.email4,
                               m_emails.username5, m_emails.email5]) if m_emails else False

    cp_email_data_exists = any([cp_emails.username1, cp_emails.email1,
                                cp_emails.username2, cp_emails.email2,
                                cp_emails.username3, cp_emails.email3,
                                cp_emails.username4, cp_emails.email4,
                                cp_emails.username5, cp_emails.email5]) if cp_emails else False

    c_email_data_exists = any([email.client_id for email in c_emails]) if c_emails else False

    if request.method == 'POST':
        # Check if the form for Manil Emails was submitted
        if 'm_username1' in request.POST:
            m_emails.username1 = request.POST.get('m_username1')
            m_emails.email1 = request.POST.get('m_email1')
            m_emails.username2 = request.POST.get('m_username2')
            m_emails.email2 = request.POST.get('m_email2')
            m_emails.username3 = request.POST.get('m_username3')
            m_emails.email3 = request.POST.get('m_email3')
            m_emails.username4 = request.POST.get('m_username4')
            m_emails.email4 = request.POST.get('m_email4')
            m_emails.username5 = request.POST.get('m_username5')
            m_emails.email5 = request.POST.get('m_email5')
            m_emails.save()
            return redirect('manil_emails')  # Redirect after updating Manil Emails

        # Check if the form for Chaipoint Emails was submitted
        elif 'cp_username1' in request.POST:
            cp_emails.username1 = request.POST.get('cp_username1')
            cp_emails.email1 = request.POST.get('cp_email1')
            cp_emails.username2 = request.POST.get('cp_username2')
            cp_emails.email2 = request.POST.get('cp_email2')
            cp_emails.username3 = request.POST.get('cp_username3')
            cp_emails.email3 = request.POST.get('cp_email3')
            cp_emails.username4 = request.POST.get('cp_username4')
            cp_emails.email4 = request.POST.get('cp_email4')
            cp_emails.username5 = request.POST.get('cp_username5')
            cp_emails.email5 = request.POST.get('cp_email5')
            cp_emails.save()
            return redirect('manil_emails')  # Redirect after updating Chaipoint Emails

        # Handle form for Client Emails based on client_id (primary key)
        elif 'client_id' in request.POST:
            client_id = request.POST.get('client_id')

            # Check if emails already exist for the selected client_id
            c_emails_instance, created = Client_emails.objects.update_or_create(
                client_id=client_id,
                defaults={
                    'username1': request.POST.get('c_username1'),
                    'email1': request.POST.get('c_email1'),
                    'username2': request.POST.get('c_username2'),
                    'email2': request.POST.get('c_email2'),
                    'username3': request.POST.get('c_username3'),
                    'email3': request.POST.get('c_email3'),
                    'username4': request.POST.get('c_username4'),
                    'email4': request.POST.get('c_email4'),
                    'username5': request.POST.get('c_username5'),
                    'email5': request.POST.get('c_email5')
                }
            )
            return redirect('manil_emails') 

    context = {
        'data': data,
        'clients': clients,
        'm_emails': m_emails,
        'cp_emails': cp_emails,
        'c_emails': c_emails,
        'selected_client_id' : selected_client_id,
        'm_email_data_exists': m_email_data_exists,
        'cp_email_data_exists': cp_email_data_exists,
        'c_email_data_exists': c_email_data_exists,
    }

    return render(request, 'manil_temp/manil_emails.html', context)


def manil_user(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)
    m_user = Manil_User.objects.all()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_id_new = request.POST.get('user_id')
        phone_number = request.POST.get('phone_number')
        email_id = request.POST.get('email_id')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        context = {
            'first_name': first_name, 'last_name': last_name, 'user_id': user_id_new, 'role': role
        }

        for i in m_user:
            if i.user_id == user_id_new:
                messages.error(request, 'This user ID is already in use.')
                return render(request, 'manil_temp/manil_user.html', {'data': data, 'm_user': m_user, **context})

        if password != confirm_password:
            messages.error(request, 'Password mismatch, Please try again.')
            return render(request, 'manil_temp/manil_user.html', {'data': data, 'm_user': m_user, **context})

        # Save new user
        Manil_User_new = Manil_User(
            user_id=user_id_new,
            first_name=first_name,
            last_name=last_name,
            role=role,
            email_id=email_id,
            phone_number=phone_number,
            password=password,
            created_by=data.first_name + data.last_name,
            creation_date=timezone.now() + timedelta(hours=5, minutes=30)
        )
        Manil_User_new.save()

        # Save password record
        Manil_PWD_new = Manil_PWD(
            user_id=user_id_new,
            first_name=first_name,
            password=password
        )
        Manil_PWD_new.save()

        messages.success(request, 'Manil User Added Successfully', extra_tags='add_success')
        return redirect('manil_user')

    return render(request, 'manil_temp/manil_user.html', {'data': data, 'm_user': m_user})


def m_user_profile(request, user_id):
    data = Manil_User.objects.get(user_id=user_id)
    context = {'data': data}
    return render(request, 'manil_temp/m_user_profile.html', context)

def edit_manil_user(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)

    m_user = get_object_or_404(Manil_User, id=id)

    if request.method == 'POST':
        m_user.first_name = request.POST.get('edit_first_name')
        m_user.last_name = request.POST.get('edit_last_name')
        m_user.user_id = m_user.user_id       
        m_user.role = request.POST.get('edit_role')
        m_user.phone_number = request.POST.get('edit_phone_number')
        m_user.email_id = request.POST.get('edit_email_id')
        m_user.updated_date = timezone.now() + timedelta(hours=5, minutes=30)
        m_user.updated_by = data.first_name 

        m_user.save()

        messages.success(request, 'Manil User details updated successfully.')
        return redirect('manil_user')

    return render(request, 'manil_temp/manil_user.html', {'data': data, 'm_user': m_user})


def get_short_form(text):
    words = text.split()
    
    # If the text has more than one word, take the first letter of each word
    if len(words) > 1:
        return ''.join([word[0].upper() for word in words])
    
    # If the text has only one word
    single_word = words[0]
    
    # If the word length is more than 3 characters, take the first and last character
    if len(single_word) > 3:
        return (single_word[0] + single_word[-1]).upper()
    
    # If the word length is 3 or fewer characters, take the entire word
    return single_word.upper()

def generate_client_id(client_name, client_location):
    # Get short forms of client_name and client_location
    name_1 = get_short_form(client_name)
    name_2 = get_short_form(client_location)

    # Pattern to match existing client_id
    pattern = f"{name_1}{name_2}"

    # Query to find all client_id that start with the pattern
    com_users = Client_Master.objects.filter(client_id__startswith=pattern)

    if com_users.exists():
        # Extract the numerical part from the client_id
        max_number = 0
        for user in com_users:
            client_id = user.client_id
            # Use regex to find the numeric suffix
            match = re.search(r'(\d+)$', client_id)
            if match:
                number = int(match.group(1))
                # Keep track of the maximum number found
                if number > max_number:
                    max_number = number

        # Increment the maximum number by 1
        next_number = max_number + 1
        # Ensure the number is formatted with leading zeros (e.g., 001, 010)
        new_id = f"{pattern}{str(next_number).zfill(3)}"
    else:
        # If no match is found, start with 001
        new_id = f"{pattern}001"

    return new_id

def Client_master(request):    
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)

    client_m = Client_Master.objects.all()

    all_s_name = Client_short_name.objects.all()

    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        phone_number = request.POST.get('phone_number')
        email_id = request.POST.get('email_id')
        client_location = request.POST.get('client_location')
        pan = request.POST.get('pan')
        contact_person_name = request.POST.get('contact_person_name')        
        fssai_number = request.POST.get('fssai_number') 
        client_S_name = request.POST.get('client_S_name') 
        
        billing_address = request.POST.get('billing_address')
        billing_city = request.POST.get('billing_city') 
        billing_state = request.POST.get('billing_state')         
        billing_pin = request.POST.get('billing_pin') 
        billing_gst_number = request.POST.get('billing_gst_number')

        shipping_address = request.POST.get('shipping_address')
        shipping_city = request.POST.get('shipping_city')         
        shipping_state = request.POST.get('shipping_state') 
        shipping_pin = request.POST.get('shipping_pin')
        shipping_gst_number = request.POST.get('shipping_gst_number')

        sameAsBilling = request.POST.get('sameAsBilling')         

        if sameAsBilling == 'on':
            new_shipping_city = billing_city
            new_shipping_state = billing_state
            new_shipping_pin = billing_pin
            new_shipping_address = billing_address
            new_shipping_gst_number = billing_gst_number
        else:
            new_shipping_city = shipping_city
            new_shipping_state = shipping_state
            new_shipping_pin = shipping_pin
            new_shipping_address = shipping_address
            new_shipping_gst_number = shipping_gst_number
        
            

        context = {
            'client_name':client_name, 'phone_number':phone_number,
            'email_id':email_id, 'client_location':client_location, 
            'pan':pan, 'contact_person_name':contact_person_name,
            'billing_gst_number':billing_gst_number, 'shipping_gst_number':shipping_gst_number,
            'billing_address':billing_address, 'shipping_address':shipping_address,
            'fssai_number':fssai_number, 'client_S_name':client_S_name, 
            'billing_city':billing_city, 'billing_state':billing_state, 'billing_pin':billing_pin,
            'shipping_city':shipping_city, 'shipping_state':shipping_state, 'shipping_pin':shipping_pin
        }

        # client_id = generate_client_id(client_name, client_location)

        try:
            ex_client_s = Client_short_name.objects.filter(client_S_name = client_S_name).last()
            
            prefix = ''.join([char for char in ex_client_s.client_id if not char.isdigit()])  # Extract prefix (non-numeric part)
            numeric_part = ''.join([char for char in ex_client_s.client_id if char.isdigit()])  # Extract numeric part                    
            new_number = str(int(numeric_part) + 1).zfill(len(numeric_part))                
            new_client_id = prefix + new_number
        except:
            ex_client_s = None
            new_client_id = client_S_name + '01'

        
        new_Client = Client_Master(
            client_id = new_client_id,
            client_name = client_name,
            client_S_name = client_S_name,
            client_location = client_location,            
            fssai_number = fssai_number,
            contact_person_name = contact_person_name,
            email_id = email_id,
            phone_number = phone_number,                
            pan = pan,            

            billing_address = billing_address,
            billing_city = billing_city,
            billing_state = billing_state,
            billing_pin = billing_pin,
            billing_gst_number = billing_gst_number,

            shipping_address = new_shipping_address,
            shipping_city = new_shipping_city,
            shipping_state = new_shipping_state,
            shipping_pin = new_shipping_pin,
            shipping_gst_number = new_shipping_gst_number,
        
            created_by = data.first_name,
            creation_date = timezone.now() + timedelta(hours=5, minutes=30)
        )
        new_Client.save()

        Client_s_name_n = Client_short_name(
            client_name = client_name,
            client_id = new_client_id,
            client_S_name = client_S_name
        )
        Client_s_name_n.save()

        messages.success(request, 'Client details saved successfully.')
        return redirect('Client_master')

    return render (request, 'manil_temp/Client_master.html', {'data':data, 'all_s_name':all_s_name, 'client_m':client_m})


def edit_client_master(request, id):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)

    client_m = get_object_or_404(Client_Master, id=id) 
    all_s_name = Client_short_name.objects.all()

    c_users=Client_user.objects.filter(client_id=client_m.client_id)

    if request.method == 'POST':
        client_name = request.POST.get('edit_client_name')
        phone_number = request.POST.get('edit_phone_number')
        email_id = request.POST.get('edit_email_id')
        client_location = request.POST.get('edit_client_location')
        pan = request.POST.get('edit_pan')
        contact_person_name = request.POST.get('edit_c_person')        
        fssai_number = request.POST.get('edit_fssai_number') 
        client_S_name = request.POST.get('edit_client_S_name') 
        
        billing_address = request.POST.get('edit_billing_address')
        billing_city = request.POST.get('edit_billing_city') 
        billing_state = request.POST.get('edit_billing_state')         
        billing_pin = request.POST.get('edit_billing_pin') 
        billing_gst_number = request.POST.get('edit_billing_gst_number')

        shipping_address = request.POST.get('edit_shipping_address')
        shipping_city = request.POST.get('edit_shipping_city')         
        shipping_state = request.POST.get('edit_shipping_state') 
        shipping_pin = request.POST.get('edit_shipping_pin')
        shipping_gst_number = request.POST.get('edit_shipping_gst_number')

        client_m.client_name=client_name
        client_m.phone_number=phone_number
        client_m.email_id=email_id
        client_m.client_location=client_location
        client_m.pan=pan,
        client_m.contact_person_name=contact_person_name
        client_m.fssai_number=fssai_number
        client_m.client_S_name=client_S_name
        client_m.billing_address=billing_address
        client_m.billing_city=billing_city
        client_m.billing_state=billing_state
        client_m.billing_pin=billing_pin
        client_m.billing_gst_number=billing_gst_number
        client_m.shipping_address=shipping_address
        client_m.shipping_city=shipping_city
        client_m.shipping_state=shipping_state
        client_m.shipping_pin=shipping_pin
        client_m.shipping_gst_number=shipping_gst_number
        client_m.upadated_date = timezone.now() + timedelta(hours=5, minutes=30)
        client_m.updated_by = data.first_name 

        client_m.save()
        
        # Update related Robot_Details fields
        # Client_user.objects.filter(client_id=client_m.client_id).update(
        #    client_name = client_name
        # )

        messages.success(request, 'Client Master details updated successfully.')
        return redirect ('Client_master')

    return render (request, 'manil_temp/Client_master.html', {'data':data, 'all_s_name':all_s_name, 'client_m':client_m})


def get_sname_matches(request):
    query = request.GET.get('query', '')
    if query:
        
        matches = Client_short_name.objects.filter(client_S_name__icontains=query).values_list('client_S_name', flat=True).distinct()
        return JsonResponse({'matches': list(matches)})
    
    return JsonResponse({'matches': []})


def cust_user_master(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)

    client_m = Client_Master.objects.all()
    com_user = Client_user.objects.all()
    

    context = {'data': data, 'client_m': client_m, 'com_user': com_user}

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email_id = request.POST.get('email_id')
        role = request.POST.get('role')        
        client_id = request.POST.get('client_id')

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        context_2 = {
            'first_name': first_name, 'last_name': last_name, 'phone_number': phone_number, 'email_id': email_id, 
            'role': role, 'client_id': client_id
        }

        # Merging the context dictionaries
        combined_context = {**context, **context_2}

        if password != confirm_password:
            messages.error(request, 'Password mismatch, Please try again.')
            return render(request, 'manil_temp/cust_user_master.html', combined_context)

        client_dt = Client_Master.objects.get(client_id=client_id)

        try:
            exist_user = Client_user.objects.filter(client_id=client_id).last()

            prefix = exist_user.user_id.split('_u')[0]  
            numeric_part = exist_user.user_id.split('_u')[1]             
            new_number = str(int(numeric_part) + 1).zfill(len(numeric_part))            
            new_user_id = f"{prefix}_u{new_number}"

        except:
            exist_user = None
            new_user_id = f"{client_dt.client_id}_u01"
        
        Client_user_new = Client_user(
            user_id=new_user_id,
            first_name=first_name,
            last_name=last_name,
            client_id=client_id,
            client_name=client_dt.client_name,
            role=role,            
            email_id=email_id,
            phone_number=phone_number,
            password=password,
            pwd_date=timezone.now() + timedelta(hours=5, minutes=30),
            creation_date=timezone.now() + timedelta(hours=5, minutes=30),
            created_by=data.first_name
        )
        Client_user_new.save()      

        Client_PWD_new = Client_PWD(
            user_id = new_user_id,
            first_name = first_name,
            password = password
        )       
        Client_PWD_new.save() 

        messages.success(request, 'Client User Added Successfully', extra_tags='add_success')
        return render(request, 'manil_temp/cust_user_master.html', combined_context)

    return render(request, 'manil_temp/cust_user_master.html', context)


def edit_cust_user(request, id):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)

    client_m = Client_Master.objects.all()
    com_user = get_object_or_404(Client_user, id=id)

    if request.method == 'POST':
        com_user.first_name = request.POST.get('edit_first_name')
        com_user.last_name = request.POST.get('edit_last_name')
        com_user.phone_number = request.POST.get('edit_phone_number')
        com_user.email_id = request.POST.get('edit_email_id')
        com_user.role = request.POST.get('edit_role')        
        com_user.client_id = com_user.client_id
        
        com_user.updated_date = timezone.now() + timedelta(hours=5, minutes=30)
        com_user.updated_by = data.first_name 
        
        com_user.save()
        
        messages.success(request, 'Client User Details are Updated')
        return redirect ('cust_user_master')
         
    return render(request, 'manil_temp/cust_user_master.html', {'data': data, 'client_m': client_m, 'com_user': com_user})


def material_master(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)

    
    materials = Material_Master.objects.all()
    
    if request.method == 'POST':
        material_name = request.POST.get('material_name')        
        hsn_code = request.POST.get('hsn_code')
        unit_of_measurement = request.POST.get('unit_of_measurement')
        Base_Price = request.POST.get('Base_Price')
        cgst_rate = Decimal(request.POST.get('cgst_rate'))
        sgst_rate = Decimal(request.POST.get('sgst_rate'))
        igst_rate = request.POST.get('igst_rate')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')    
        conversion_rate = request.POST.get('conversion_rate')
        
        #print('cgst_rate', cgst_rate)   

        context = {
            'material_name':material_name, 'hsn_code':hsn_code, 'unit_of_measurement':unit_of_measurement, 'Base_Price':Base_Price, 'cgst_rate':cgst_rate, 'sgst_rate':sgst_rate,
            'igst_rate':igst_rate, 'start_date':start_date, 'end_date':end_date
        }

        if materials.exists():
            for i in materials:
                if i.hsn_code == hsn_code:
                    messages.error(request, 'This HNS Code is already in use.')
                    return render(request, 'manil_temp/material_master.html', {'data':data,'materials': materials, **context})

        if materials.exists():            
            last_name = materials.last().material_code                       
            pre = last_name[:-3]  
            suf = int(last_name[-3:])                        
            new_suf = suf + 1
                    
            new_suffix = f"{new_suf:03}"        
            new_value = pre + new_suffix
        else:           
            new_value = 'MAT001'
        

        
        new_material = Material_Master(
            material_code=new_value,
            hsn_code=hsn_code,
            material_name=material_name,
            unit_of_measurement=unit_of_measurement,
            Base_Price=Base_Price,
            cgst_rate=cgst_rate,
            sgst_rate=sgst_rate,
            igst_rate=igst_rate,
            start_date=start_date,
            end_date=end_date,
            creation_date=timezone.now() + timedelta(hours=5, minutes=30),
            created_by=data.first_name, # Assuming you have user authentication
            conversion_rate = conversion_rate
        )
        new_material.save()

        messages.success(request, 'Material added successfully.')
        return redirect('material_master')
    
    return render(request, 'manil_temp/material_master.html', {'data':data,'materials': materials})


def edit_material_master(request, id):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)

    materials = get_object_or_404(Material_Master, id=id)

    if request.method == 'POST':
        materials.material_name = materials.material_name     
        materials.hsn_code = request.POST.get('edit_hsn_code')
        materials.unit_of_measurement = request.POST.get('edit_uom')
        materials.conversion_rate = request.POST.get('edit_conversion_rate')
        materials.Base_Price = request.POST.get('edit_Base_Price')
        materials.cgst_rate = Decimal(request.POST.get('edit_cgst_rate'))
        materials.sgst_rate = Decimal(request.POST.get('edit_sgst_rate'))
        materials.igst_rate = request.POST.get('edit_igst_rate')
        materials.start_date = request.POST.get('edit_start_date')
        materials.end_date = request.POST.get('edit_end_date')
        materials.updated_date = timezone.now() + timedelta(hours=5, minutes=30)
        materials.updated_by = data.first_name 
 
        materials.save()
        messages.success(request, 'Material Details are Updated')
        return redirect('material_master')
    
    return render(request, 'manil_temp/material_master.html', {'data':data,'materials': materials})


def material_cost(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)

    client_m = Client_Master.objects.all()

    costings = Costing_Table.objects.all()
    materials = Material_Master.objects.all()

    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        client_name = request.POST.get('client_name')
        client_location = request.POST.get('client_location')
        material_code = request.POST.get('material_code') 
        material_name = request.POST.get('material_name')        
        hsn_code = request.POST.get('hsn_code')      
        
        cost_per_unit = request.POST.get('cost_per_unit')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        unit_of_measurement = request.POST.get('unit_of_measurement')

        mat_rec = Material_Master.objects.get(material_code = material_code)
               
         
        new_costing = Costing_Table(
            client_id=client_id,  
            client_name = client_name,
            location=client_location,
            material_code=material_code, 
            material_name = material_name,  
            hsn_code = hsn_code,                     
            cost_per_unit=int(cost_per_unit),
            start_date=start_date,
            end_date=end_date,
            creation_date=timezone.now() + timedelta(hours=5, minutes=30),
            created_by=data.first_name,

            unit_of_measurement= unit_of_measurement,
            conversion_rate = mat_rec.conversion_rate,
            Base_Price=mat_rec.Base_Price,
            cgst_rate=mat_rec.cgst_rate,
            sgst_rate=mat_rec.sgst_rate,
            igst_rate=mat_rec.igst_rate,
            
        )
        new_costing.save()

        messages.success(request, 'Material cost for a client added successfully')
        return redirect('material_cost')
    
    return render(request, 'manil_temp/material_cost.html', {'data': data, 'costings': costings, 'materials': materials, 'client_m':client_m})

def edit_material_cost(request,id):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)

    client_m = Client_Master.objects.all()
    materials = Material_Master.objects.all()

    costings = get_object_or_404 (Costing_Table, id=id)

    if request.method == 'POST':
        costings.client_id = costings.client_id
        costings.client_name = costings.client_name
        costings.material_code = costings.material_code 
        costings.material_name = costings.material_name  
        
        costings.unit_of_measurement = request.POST.get('edit_uom')
        costings.cost_per_unit = request.POST.get('edit_cost_per_unit')
        costings.start_date = request.POST.get('edit_start_date')
        costings.end_date = request.POST.get('edit_end_date')

        costings.updated_date = timezone.now() + timedelta(hours=5, minutes=30)
        costings.updated_by = data.first_name 

        costings.save()

        messages.success(request, 'Material cost for a client updated successfully')
        return redirect('material_cost')
    
    return render(request, 'manil_temp/material_cost.html', {'data': data, 'costings': costings, 'materials': materials, 'client_m':client_m})


def manil_order_(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)

    m_orders = manil_order.objects.all()


    return render (request, 'manil_temp/manil_order.html', {'data':data, 'm_orders':m_orders})

def client_order_(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)
    all_orders = client_order.objects.all()
    
    order_details = client_order_details.objects.all()

    all_client = Client_Master.objects.all()
    all_users = Client_user.objects.all()
    cost_det = Costing_Table.objects.all()
    mat_list = Material_Master.objects.all()
    

    context = {
        'data': data,
        'all_orders': all_orders,
        'order_details':order_details,
        'mat_list': mat_list,
        'all_client': all_client,
        'all_users': all_users,
        'cost_det': cost_det,
    }

    if request.method == 'POST':
        no_of_sec = request.POST.get('no_of_sec')
        client_id = request.POST.get('client_id')
        po_authority = request.POST.get('po_authority')
        po_authority_date = request.POST.get('po_authority_date')
        shipping_address = request.POST.get('shipping_address')
        shipping_city = request.POST.get('shipping_city')
        shipping_state = request.POST.get('shipping_state')
        shipping_pin = request.POST.get('shipping_pin')
        amt_in_words = request.POST.get('amt_in_words')
        grand_total = request.POST.get('grand_total')

        # Generate a new order number
        if all_orders.exists():
            last_num = all_orders.last().order_number
            pre = last_num[:-3]
            suf = int(last_num[-3:])
            new_suf = suf + 1
            new_value = pre + f"{new_suf:03}"
        else:
            new_value = 'ORD001'

        # Save order details
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
                order_number=new_value,
                material_name=material_name,
                hsn_code = hsn_code,
                uom=uom,
                qty=qty,
                base_price=base_price,
                gst_type=gst_type,
                gst_rate=gst_rate,
                gst_amt=round(float(gst_amt)),
                sub_total=round(float(sub_total)),
            )
            order_details_n.save()

        # Save the main order
        client_dt = Client_Master.objects.get(client_id=client_id)
        client_order_new = client_order(
            client_id=client_id,
            client_name=client_dt.client_name,
            order_number=new_value,
            order_date=timezone.now() + timedelta(hours=5, minutes=30),
            po_authority=po_authority,
            po_authority_date=po_authority_date,
            creation_date=timezone.now() + timedelta(hours=5, minutes=30),
            created_by=data.first_name,
            grand_total=round(float(grand_total)),
            ammount_words=amt_in_words,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_state=shipping_state,
            shipping_pin=shipping_pin,
            status='Order Placed',
        )
        client_order_new.save()

        notification_message = f"Your order has been placed successfully on {timezone.now().strftime('%d-%m-%Y %H:%M')}."
        notification_title = f"Order Update"

        # Create a new notification for the logged-in user
        notification = Notification(
            created_by = data.user_id,
            message=notification_message,
            title = notification_title
        )
        notification.save()

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
        client_email_objs = Client_emails.objects.filter(client_id=client_id)  # Fetch all matching client_id entries
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
        <p>Dear {client_dt.client_name},</p>
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

        messages.success(request, 'Your order has been placed.')
        return redirect('client_order_')

    return render(request, 'manil_temp/client_order.html', context)

from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def edit_client_order(request, order_number):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)
    order = get_object_or_404(client_order, order_number=order_number)
    order_details = client_order_details.objects.filter(order_number=order_number)
    
    all_client = Client_Master.objects.all()
    all_users = Client_user.objects.all()
    cost_det = Costing_Table.objects.all()
    mat_list = Material_Master.objects.all()
    
    context = {
        'data': data,
        'order': order,
        'order_details': order_details,
        'mat_list': mat_list,
        'all_client': all_client,
        'all_users': all_users,
        'cost_det': cost_det,
    }
    
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        po_authority = request.POST.get('po_authority')
        po_authority_date = request.POST.get('po_authority_date')
        shipping_address = request.POST.get('shipping_address')
        shipping_city = request.POST.get('shipping_city')
        shipping_state = request.POST.get('shipping_state')
        shipping_pin = request.POST.get('shipping_pin')
        amt_in_words = request.POST.get('amt_in_words')
        grand_total = request.POST.get('grand_total')
        no_of_sec = request.POST.get('no_of_sec')

        # Update main order
        order.client_id = client_id
        client_dt = Client_Master.objects.get(client_id=client_id)
        order.client_name = client_dt.client_name
        order.po_authority = po_authority
        order.po_authority_date = po_authority_date
        order.shipping_address = shipping_address
        order.shipping_city = shipping_city
        order.shipping_state = shipping_state
        order.shipping_pin = shipping_pin
        order.grand_total = round(float(grand_total))
        order.ammount_words = amt_in_words
        order.status = 'Order Placed'
        order.save()

        # Update order details
        order_details.delete()  # Remove old order details
        
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
                order_number=order_number,
                material_name=material_name,
                uom=uom,
                qty=qty,
                base_price=base_price,
                gst_type=gst_type,
                gst_rate=gst_rate,
                gst_amt=round(float(gst_amt)),
                sub_total=round(float(sub_total)),
            )
            order_details_n.save()

        messages.success(request, 'Order has been updated successfully.')
        return redirect('client_order_')

    return render(request, 'manil_temp/client_order.html', context)

def c_order_view(request, ord_no):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)

    all_orders = manil_order.objects.all()
    order = client_order.objects.get(order_number=ord_no)
    ord_det = client_order_details.objects.filter(order_number=ord_no)
    client_det = Client_Master.objects.get(client_id=order.client_id)
    mat_list = Material_Master.objects.all()
    
    new_values = {}
    grand_total = 0

    for i in ord_det:
        for j in mat_list:
            if i.material_name == j.material_name:
                new_qty = i.qty * j.conversion_rate
                sub_total = new_qty * j.Base_Price
                sub_total = round(sub_total + (sub_total * (i.gst_rate / 100)))

                # Initialize dictionary entry if not exists
                if i.material_name not in new_values:
                    new_values[i.material_name] = {}

                # Assign values
                new_values[i.material_name]['qty'] = new_qty
                new_values[i.material_name]['sub_total'] = sub_total

    for key, value in new_values.items():
        grand_total += value['sub_total']

    grand_total_word = num2words(grand_total).title()

    if request.method == "POST":

        order_number = request.POST.get('order_number')
        old_order = client_order.objects.get(order_number=order_number)
        amt_in_words = request.POST.get('amt_in_words')
        grand_total = request.POST.get('grand_total')                

        if all_orders.exists():            
            last_num = all_orders.last().process_num                       
            pre = last_num[:-3]  
            suf = int(last_num[-3:]) 
            new_suf = suf + 1 
            
            if new_suf > 999:                
                new_suffix = f"{new_suf}" 
            else:
                new_suffix = f"{new_suf:03}"             
            new_value = pre + new_suffix
        else:           
            new_value = 'PRS001' 
       
        manil_order_new = manil_order(
            process_num=new_value,
            client_id=old_order.client_id,   
            client_name=old_order.client_name,           
            order_number=old_order.order_number,
            order_date=old_order.order_date,
            po_authority=old_order.po_authority,
            po_authority_date=old_order.po_authority_date,
            creation_date=timezone.now() + timedelta(hours=5, minutes=30),
            created_by=data.first_name,
            grand_total=round(float(grand_total)),
            ammount_words=amt_in_words, 

            shipping_address=old_order.shipping_address,
            shipping_city=old_order.shipping_city,
            shipping_state=old_order.shipping_state,
            shipping_pin=old_order.shipping_pin,
            status='Order Placed'
        )
        manil_order_new.save()

        # Update old order status
        old_order.status = 'In Progress'
        old_order.authorisation_date = timezone.now() + timedelta(hours=5, minutes=30)
        old_order.authorised_by = data.first_name
        old_order.save()

        for i in ord_det:
            material = Material_Master.objects.get(material_name=i.material_name)
            gst_amount = round(i.qty * material.conversion_rate * material.Base_Price * (i.gst_rate / 100))
            sub_total = round(i.qty * material.conversion_rate * material.Base_Price + gst_amount)

            manil_order_details.objects.create(
                process_num=manil_order_new.process_num,
                material_name=i.material_name,
                hsn_code=material.hsn_code,
                uom=material.unit_of_measurement,
                qty=i.qty * material.conversion_rate,
                base_price=material.Base_Price,
                gst_type=i.gst_type,
                gst_rate=i.gst_rate,
                gst_amt=gst_amount,
                sub_total=sub_total
            )

        # Prepare email details
        order_details_rows = ""
        for idx, i in enumerate(ord_det, start=1):
            material = Material_Master.objects.get(material_name=i.material_name)
            gst_amount = round(i.qty * material.conversion_rate * material.Base_Price * (i.gst_rate / 100))
            sub_total = round(i.qty * material.conversion_rate * material.Base_Price + gst_amount)
            
            order_details_rows += f"""
            <tr>
                <td>{idx}</td>
                <td>{i.material_name}</td>
                <td>{i.qty * material.conversion_rate}</td>
                <td>{material.unit_of_measurement}</td>
                <td>{material.Base_Price}</td>
                <td>{i.gst_rate}%</td>
                <td>{gst_amount}</td>
                <td>{sub_total}</td>
            </tr>
            """

        email_body = f"""
        <p>Dear Manil Team,</p>
        <p>The order has been successfully processed. Here are the details:</p>

        <h3>Order Summary</h3>
        <p><strong>Order Number:</strong> {new_value}</p>

        <h3>Order Details</h3>
        <table border="1" style="border-collapse: collapse; width: 100%; text-align: left;">
            <thead>
                <tr>
                    <th>S.No</th>
                    <th>Material Name</th>
                    <th>Quantity</th>
                    <th>UOM</th>
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
        <p><strong>Amount in Words:</strong> {amt_in_words}</p>
        <p>Thank you!</p>
        """

        # Fetch email recipients
        manil_email_obj = Manil_emails.objects.first()
        chaipoint_email_obj = Chaipoint_emails.objects.first()

        manil_emails = [
            manil_email_obj.email1,
            manil_email_obj.email2,
            manil_email_obj.email3,
            manil_email_obj.email4,
            manil_email_obj.email5
        ] if manil_email_obj else []

        chaipoint_emails = [
            chaipoint_email_obj.email1,
            chaipoint_email_obj.email2,
            chaipoint_email_obj.email3,
            chaipoint_email_obj.email4,
            chaipoint_email_obj.email5
        ] if chaipoint_email_obj else []

        recipient_list = manil_emails + chaipoint_emails

        # Send email
        email = EmailMessage(
            subject='Order Processed Notification',
            body=email_body,
            from_email=settings.EMAIL_HOST_USER,
            to=recipient_list,
        )
        email.content_subtype = 'html'
        email.send(fail_silently=False)

        messages.success(request, "Your order has been placed.")
        return redirect('manil_order_')

    context = {
        'data': data,
        'order': order,
        'ord_det': ord_det,
        'client_det':client_det,
        'mat_list': mat_list,
        'new_values': new_values,
        'grand_total': grand_total,
        'grand_total_word': f"{grand_total_word} Rupees Only"
    }

    return render(request, 'manil_temp/c_order_view.html', context)



def manil_dispatch(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)

    dispatch = Despatch_Details.objects.all()

    return render (request, 'manil_temp/manil_dispatch.html', {'data':data, 'dispatch':dispatch})


def chaipoint_user(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)

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
        
    return render (request, 'manil_temp/chaipoint_user.html', context)

def edit_chaipoint_user(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)

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
        return redirect('chaipoint_user')

    return render(request, 'manil_temp/chaipoint_user.html', {'data': data, 'cp_user': cp_user})

def manil_ticket(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)

    tickets = Robo_Ticket.objects.all()

    return render (request, 'manil_temp/manil_ticket.html', {'data':data, 'tickets':tickets})

def ticket_view(request,ticket_num):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)

    tickets=Robo_Ticket.objects.get(ticket_num=ticket_num)
    client_dt=Client_Master.objects.get(client_id=tickets.client_id)

    if request.method == 'POST':
        tickets.res_description = request.POST.get('res_description')
        tickets.resolved_by = data.first_name
        tickets.resolved_dt = timezone.now() + timedelta(hours=5, minutes=30)
        tickets.status = 'In Progress'

        tickets.save()

        messages.success(request, "Ticket Has been solved")
        return redirect ('manil_ticket')
    
    return render (request, 'manil_temp/ticket_view.html', {'data':data,'tickets':tickets,'client_dt':client_dt,})

def robo_master(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)
    robots = Robot_Master.objects.all()

    if request.method == 'POST':        
        robot_name = request.POST.get('robo_name')
        robot_type = request.POST.get('robot_type')
        description = request.POST.get('description')

        if robots.exists():            
            last_id = robots.last().robot_id                       
            pre = last_id[:-3]  
            suf = int(last_id[-3:])                        
            new_suf = suf + 1
                    
            new_suffix = f"{new_suf:03}"        
            new_value = pre + new_suffix
        else:           
            new_value = 'ROBO001'


        # Create a new robot entry
        new_robot = Robot_Master(
            robot_id=new_value,
            robot_name=robot_name,
            robot_type=robot_type,
            description=description,
            creation_date=timezone.now() + timedelta(hours=5, minutes=30),
            created_by=data.first_name
        )
        new_robot.save()

        messages.success(request, "Robot is added successfully.")
        return redirect ('robo_master')

    return render(request, 'manil_temp/robo_master.html', {'robots': robots,'data': data})


def edit_robot_master(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)

    # Get the Robot_Master object
    robots = get_object_or_404(Robot_Master, id=id)

    if request.method == 'POST':
        # Update Robot_Master fields
        updated_robot_name = request.POST.get('edit_robo_name')
        updated_robot_type = request.POST.get('edit_robot_type')
        updated_description = request.POST.get('edit_description')

        robots.robot_name = updated_robot_name
        robots.robot_type = updated_robot_type
        robots.description = updated_description
        robots.updated_date = timezone.now() + timedelta(hours=5, minutes=30)
        robots.updated_by = data.first_name
        robots.save()

        # Update related Robot_Details fields
        Robot_Details.objects.filter(robot_id=robots.robot_id).update(
            robot_name=updated_robot_name,
            robot_type=updated_robot_type,
        )

        messages.success(request, "Robot Details are Updated successfully.")
        return redirect('robo_master')

    return render(request, 'manil_temp/robo_master.html', {'robots': robots, 'data': data})


def robo_details(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)


    client_m = Client_Master.objects.all()
    robots = Robot_Master.objects.all()
    robot_details = Robot_Details.objects.all()

    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        client_name = request.POST.get('client_name')
        location = request.POST.get('location')
        robot_id = request.POST.get('robot_id')
        robot_name = request.POST.get('robot_name')
        robot_type = request.POST.get('robot_type')
        installation_date = request.POST.get('installation_date')
        l_maintenance_date = request.POST.get('l_maintenance_date')
        status = request.POST.get('status')
        description = request.POST.get('description')

        

        # Create a new Robot_Details entry
        new_robot_detail = Robot_Details(
            client_id=client_id,
            client_name=client_name,
            location=location,
            robot_id=robot_id,
            robot_name=robot_name,
            robot_type=robot_type,
            installation_date=installation_date,
            l_maintenance_date=l_maintenance_date,
            status=status,
            description=description,
            creation_date=timezone.now() + timedelta(hours=5, minutes=30),
            created_by=data.first_name
        )
        new_robot_detail.save()
        messages.success(request, "Robot details are added successfully.")
        return redirect ('robo_details')
    
    return render(request, 'manil_temp/robo_details.html', {'client_m': client_m, 'robots': robots, 'robot_details': robot_details,'data': data })

def edit_robo_details(request, id):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)


    client_m = Client_Master.objects.all()
    robots = Robot_Master.objects.all()
    robot_details = get_object_or_404(Robot_Details, id=id)

    if request.method == 'POST':
        robot_details.client_id = request.POST.get('edit_client_id')
        robot_details.client_name = request.POST.get('edit_client_name')
        robot_details.location = request.POST.get('edit_location')
        robot_details.robot_id = request.POST.get('edit_robot_id')
        robot_details.robot_name = request.POST.get('edit_robot_name')
        robot_details.robot_type = request.POST.get('edit_robot_type')
        robot_details.installation_date = request.POST.get('edit_installation_date')
        robot_details.l_maintenance_date = request.POST.get('edit_l_maintenance_date')
        robot_details.status = request.POST.get('edit_status')
        robot_details.description = request.POST.get('edit_description')
        robot_details.save()

        messages.success(request, "Robot details are Updated successfully.")
        return redirect ('robo_details')
    
    return render(request, 'manil_temp/robo_details.html', {'client_m': client_m, 'robots': robots, 'robot_details': robot_details,'data': data })


def calculate_financial_year(current_date):
    current_year = current_date.year
    current_month = current_date.month

    if current_month >= 4:
        return date(current_year, 4, 1), date(current_year + 1, 3, 31)
    else:
        return date(current_year - 1, 4, 1), date(current_year, 3, 31)

def generate_invoice_number():
    invoices = M_client_invoice.objects.all()
    current_date = timezone.now() + timedelta(hours=5, minutes=30)

    # Calculate financial year
    financial_year_start, financial_year_end = calculate_financial_year(current_date)
    st_year = str(financial_year_start.year)[-2:] 
    end_year = str(financial_year_end.year)[-2:]  
    fy_part = f"{st_year}{end_year}" 

    
    if invoices.exists():
        last_invoice = invoices.last().invoice_num  

       
        last_fy_part = last_invoice[10:14]  
        last_serial = int(last_invoice[-4:]) 

    
        if last_fy_part != fy_part:
            new_serial = 1
        else:
            new_serial = last_serial + 1
    else:
        new_serial = 1

   
    serial_part = f"{new_serial:04}"  

    
    return f"MANIL/MCC/{fy_part}{serial_part}"



def invoice_preview(request, ord_no):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)

    manil_det = Manil_db.objects.first()
    order = client_order.objects.get(order_number=ord_no)
    client_det = Client_Master.objects.get(client_id=order.client_id)
    ord_det = client_order_details.objects.filter(order_number=ord_no)
    mat_list = Material_Master.objects.all()
    dispatch = Despatch_Details.objects.all()

    existing_invoice = M_client_invoice.objects.filter(order_number=order.order_number).exists()

    if request.method == 'POST' and not existing_invoice:
        # Generate a new invoice number
        new_invoice_num = generate_invoice_number()

        # Save new invoice
        new_invoice = M_client_invoice(
            order_number=order.order_number,
            client_id=order.client_id,
            client_name=order.client_name,
            invoice_num=new_invoice_num,
            invoice_date=timezone.now() + timedelta(hours=5, minutes=30),
            po_authority=order.po_authority,
            total_price=order.grand_total,
            creation_date=timezone.now() + timedelta(hours=5, minutes=30),
            created_by=data.first_name,
        )
        new_invoice.save()

        # Generate PDF
        context = {
            'data': data,
            'order': order,
            'client_det': client_det,
            'ord_det': ord_det,
            'mat_list': mat_list,
            'dispatch': dispatch,
            'manil_det': manil_det,
            'invoice': new_invoice,
        }
        rendered_html = render_to_string('manil_temp/invoice_pdf.html', context)
        result = BytesIO()
        pdf = pisa.CreatePDF(BytesIO(rendered_html.encode("UTF-8")), dest=result)

        if not pdf.err:
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

            client_emails = []
            client_email_objs = Client_emails.objects.filter(client_id=order.client_id)  
            for client_email_obj in client_email_objs:
                for i in range(1, 6):  
                    email_field = f'email{i}'
                    email = getattr(client_email_obj, email_field, None)
                    if email:
                        client_emails.append(email)

            # Combine emails
            recipient_list = manil_emails + client_emails

            subject = f'Invoice Generated for Order {ord_no}'
            email_body = f"""
            <p>Dear Team,</p>
            <p>An invoice has been generated for the following order:</p>
            <ul>
                <li><strong>Order Number:</strong> {order.order_number}</li>
                <li><strong>Invoice Number:</strong> {new_invoice.invoice_num}</li>
                <li><strong>Client Name:</strong> {client_det.client_name}</li>
                <li><strong>Total Price:</strong> {order.grand_total}</li>
            </ul>
            <p>Kindly find the invoice attached.</p>
            """

            email = EmailMessage(
                subject=subject,
                body=email_body,
                from_email=settings.EMAIL_HOST_USER,
                to=recipient_list,
            )
            email.content_subtype = 'html'
            email.attach(f'invoice_{ord_no}.pdf', result.getvalue(), 'application/pdf')
            email.send(fail_silently=False)

            messages.success(request, 'Invoice generated successfully.')
            return redirect('m_invoice_table')
        else:
            messages.error(request, 'Error in generating invoice PDF.')

    context = {
        'data': data,
        'order': order,
        'client_det': client_det,
        'ord_det': ord_det,
        'mat_list': mat_list,
        'dispatch': dispatch,
        'manil_det': manil_det,
        'show_generate_button': not existing_invoice  # Show button only if no invoice
    }

    return render(request, 'manil_temp/invoice_preview.html', context)



def m_invoice_table (request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)

    invoice = M_client_invoice.objects.all()


    return render (request, 'manil_temp/invoice_table.html', {'data':data, 'invoice':invoice})

def m_invoice_view(request, ord_no):    
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)

    manil_det = Manil_db.objects.first()

    order = client_order.objects.get(order_number = ord_no)

    client_det = Client_Master.objects.get(client_id = order.client_id)

    ord_det = client_order_details.objects.filter(order_number = ord_no)

    mat_list = Material_Master.objects.all()
    
    dispatch = Despatch_Details.objects.all()

    invoice = M_client_invoice.objects.get(order_number=order.order_number)


    context = {'data':data, 'order':order, 'client_det':client_det, 'ord_det':ord_det, 'mat_list':mat_list, 'dispatch':dispatch, 'manil_det':manil_det, 'invoice':invoice }
    
    return render (request, 'manil_temp/m_invoice_view.html', context)




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

def m_download_invoice(request, ord_no):
    # Fetch data
    user_id = request.session.get('user_id')
    try:
        data = Manil_User.objects.get(user_id=user_id)
        manil_det = Manil_db.objects.first()
        order = client_order.objects.get(order_number=ord_no)
        client_det = Client_Master.objects.get(client_id=order.client_id)
        ord_det = client_order_details.objects.filter(order_number=ord_no)
        invoice = M_client_invoice.objects.get(order_number=ord_no)
    except Exception as e:
        return HttpResponse(str(e), status=404)

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


def order_remarks(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)

    tickets = Order_Tickets.objects.filter(
        remarks__isnull=False,
        remarks_title__isnull=False,
        remarked_by__isnull=False,
        remarked_date__isnull=False
    )

    return render(request, 'manil_temp/order_remarks.html', {'data': data, 'tickets': tickets})

def order_remarks_view(request, ord_no):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)

    tickets = get_object_or_404( Order_Tickets , process_num=ord_no)

    images = Remarkes_images.objects.filter(process_num=ord_no)

    return render(request, 'manil_temp/order_remarks_view.html', {'data': data,'tickets': tickets,'images': images })



def delete_manil_user(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)
    
    m_user = get_object_or_404(Manil_User, id=id)
    m_user.delete()

    messages.success(request, 'Manil User Deletd Successfully')
    return redirect('manil_user')

def delete_client_master(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)
    
    client_master = get_object_or_404(Client_Master, id=id)
    client_master.delete()

    messages.success(request, 'Client is Deletd Successfully')
    return redirect('Client_master')

def delete_client_user(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)
    
    client_user = get_object_or_404(Client_user, id=id)
    client_user.delete()

    messages.success(request, 'Client user is Deletd Successfully')
    return redirect('cust_user_master')

def delete_chaipoint_user(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)
    
    cp_user = get_object_or_404(chai_point_user, id=id)
    cp_user.delete()

    messages.success(request, 'Chaipoint user is Deletd Successfully')
    return redirect('chaipoint_user')

def delete_material(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)
    
    material = get_object_or_404(Material_Master, id=id)
    material.delete()

    messages.success(request, 'Material is Deletd Successfully')
    return redirect('material_master')

def delete_material_cost(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)
    
    m_cost = get_object_or_404(Costing_Table, id=id)
    m_cost.delete()

    messages.success(request, 'Material Cost is Deletd Successfully')
    return redirect('material_cost')

def delete_client_order(request, order_number):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)
    
    c_order = get_object_or_404(client_order, order_number=order_number)
    c_order.delete()

    c_order_details = client_order_details.objects.filter(order_number=order_number)
    c_order_details.delete()

    m_order = get_object_or_404(manil_order, order_number=c_order.order_number)
    m_order.delete()

    m_order_details = manil_order_details.objects.filter(order_number=c_order.order_number)
    m_order_details.delete()

    messages.success(request, 'Client Order is Deleted Successfully')
    return redirect('client_order_')

def delete_manil_order(request, process_num):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)
    
    m_order = get_object_or_404(manil_order, process_num=process_num)
    m_order.delete()

    m_order_details = manil_order_details.objects.filter(process_num=process_num)
    m_order_details.delete()

    c_order = get_object_or_404(client_order, order_number=m_order.order_number)
    c_order.status = "Order Placed"
    c_order.save()

    messages.success(request, 'Manil Order is Deleted Successfully')
    return redirect('manil_order_')

def delete_m_dispatch(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)
    
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

def delete_invoice(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)
    
    invoice = get_object_or_404( M_client_invoice, id=id)
    invoice.delete()

    messages.success(request, 'Invoice is Deleted Successfully')
    return redirect('m_invoice_table')

def delete_order_remark(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)
    
    order_remark = get_object_or_404( Order_Tickets, id=id)
    order_remark.delete()

    messages.success(request, 'Order Remark is Deleted Successfully')
    return redirect('order_remarks')

def delete_robot_ticket(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)
    
    robo_ticket = get_object_or_404( Robo_Ticket, id=id)
    robo_ticket.delete()

    messages.success(request, 'Robot Ticket is Deleted Successfully')
    return redirect('manil_ticket')

def delete_robot(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)
    
    robot = get_object_or_404( Robot_Master, id=id)
    robot.delete()

    robot_details = Robot_Details.objects.filter(robot_id=robot.robot_id)
    robot_details.delete()

    robo_ticket = Robo_Ticket.objects.filter(robot_id=robot.robot_id)
    robo_ticket.delete()

    messages.success(request, 'Robot is Deleted Successfully')
    return redirect('robo_master')

def delete_robot_details(request, id):
    user_id = request.session.get('user_id')
    data = get_object_or_404(Manil_User, user_id=user_id)
    
    robot_details = get_object_or_404( Robot_Details, id=id) 
    robot_details.delete()

    robo_ticket = Robo_Ticket.objects.filter(robot_id=robot_details.robot_id)
    robo_ticket.delete()

    messages.success(request, 'Robot is Deleted Successfully')
    return redirect('robo_details')


