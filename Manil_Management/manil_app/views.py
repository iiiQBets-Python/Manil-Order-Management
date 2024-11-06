
from django.shortcuts import render, get_object_or_404, redirect
from Manil_Management.imports import *

# Create your views here.
def base(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)
    return render(request, 'manil_temp/base.html',{'data':data})


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
                manil_msg = 'Login Successful!'
                return render(request, 'Base/login.html', {'manil_msg':manil_msg})                            
        if c_user:
            if check_password(password, c_user.password):
                request.session['user_id'] = c_user.user_id
                cust_msg = 'Login Successful!'
                return render(request, 'Base/login.html', {'cust_msg':cust_msg})        
        if p_user:
            if check_password(password, p_user.password):
                request.session['user_id'] = p_user.user_id
                chai_msg = 'Login Successful!'
                return render(request, 'Base/login.html', {'chai_msg':chai_msg})  
        error_msg = 'Please enter valid credentials'
        return render(request, 'Base/login.html', {'error_msg':error_msg})        
    return render(request, 'Base/login.html')

@csrf_exempt
def log_out(request):
    user_id = request.session.get('user_id')
    if user_id:
        request.session.clear()
    return redirect('login_page')

def manil_dashboard(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)

    # Orders
    c_orders = client_order.objects.all()
    total_orders = c_orders.count()
    processed_orders = c_orders.filter(status='Dispatched').count()
    pending_orders = c_orders.filter(status='Order Placed').count()
    delivered_orders = c_orders.filter(status='Delivered').count()

    # Tickets
    m_tickets = Ticket_tbl.objects.all()
    total_tickets = m_tickets.count()
    solved_tickets = m_tickets.filter(status='Closed').count()
    pending_tickets = m_tickets.filter(status='Open').count()

    context = {
        'c_orders': c_orders,
        'm_tickets': m_tickets,
        'data': data,
        'total_orders': total_orders,
        'processed_orders': processed_orders,
        'pending_orders': pending_orders,
        'delivered_orders':delivered_orders,
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
            C_data.billing_pin = request.POST.get('billing_pin')

        if 'shipping_gst_number' in request.POST:
            # Shipping Details Form (form4)
            C_data.shipping_gst_number = request.POST.get('shipping_gst_number')
            C_data.shipping_address = request.POST.get('shipping_address')
            C_data.shipping_city = request.POST.get('shipping_city')
            C_data.shipping_state = request.POST.get('shipping_state')
            C_data.shipping_pin = request.POST.get('shipping_pin')
        
        C_data.save()
    
    
    return render (request, 'manil_temp/manil_master.html', {'data':data, 'C_data':C_data})


def manil_user(request):

    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)
    m_user = Manil_User.objects.all()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_id_new = request.POST.get('user_id')        
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        context = {
           'first_name':first_name, 'last_name':last_name, 'user_id':user_id_new, 'role':role
        }

        for i in m_user:
            if i.user_id == user_id_new:
                error_msg = 'This user ID is already in use.'
                return render (request, 'manil_temp/manil_user.html', {'data':data, 'm_user':m_user, 'error_msg':error_msg, **context})
        
        if password != confirm_password:
            error_msg = 'Mismatched password.'
            return render (request, 'manil_temp/manil_user.html', {'data':data, 'm_user':m_user, 'error_msg':error_msg, **context})

        Manil_User_new = Manil_User(
            user_id = user_id_new,
            first_name = first_name,
            last_name = last_name,
            role = role,
            password = password,            
            created_by = data.user_id,
            creation_date = timezone.now() + timedelta(hours=5, minutes=30)
        )
        Manil_User_new.save()
        
        Manil_PWD_new = Manil_PWD(
            user_id = user_id_new,
            first_name = first_name,            
            password = password    
        )
        Manil_PWD_new.save()

        success_msg = 'User added successfully.'

        return render (request, 'manil_temp/manil_user.html', {'data':data, 'm_user':m_user, 'success_msg':success_msg})


    return render (request, 'manil_temp/manil_user.html', {'data':data, 'm_user':m_user})

def edit_manil_user(request, id):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)

    m_user = get_object_or_404(Manil_User, id=id)

    if request.method == 'POST':
        m_user.first_name = request.POST.get('edit_first_name')
        m_user.last_name = request.POST.get('edit_last_name')
        m_user.user_id = m_user.user_id       
        m_user.role = request.POST.get('edit_role')
        m_user.password = request.POST.get('edit_password')
        confirm_password = request.POST.get('edit_confirm_password')
        
        if m_user.password != confirm_password:
            error_msg = 'Password mismatch. Please try again.'
            return render(request, 'manil_temp/manil_user.html', {'error_msg':error_msg})
        
        m_user.upadated_date = timezone.now() + timedelta(hours=5, minutes=30)
        m_user.updated_by = data.user_id 

        m_user.save()

        return redirect('manil_user')
    return render (request, 'manil_temp/manil_user.html', {'data':data, 'm_user':m_user})


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
        
            created_by = data.user_id,
            creation_date = timezone.now() + timedelta(hours=5, minutes=30)
        )
        new_Client.save()

        Client_s_name_n = Client_short_name(
            client_name = client_name,
            client_id = new_client_id,
            client_S_name = client_S_name
        )
        Client_s_name_n.save()

        success_msg = 'Client details saved successfully'
        return render (request, 'manil_temp/Client_master.html', {'data':data, 'all_s_name':all_s_name, 'client_m':client_m, 'success_msg':success_msg})

    return render (request, 'manil_temp/Client_master.html', {'data':data, 'all_s_name':all_s_name, 'client_m':client_m})


def edit_client_master(request, id):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)

    client_m = get_object_or_404(Client_Master, id=id) 
    all_s_name = Client_short_name.objects.all()

    if request.method == 'POST':
        client_m.client_name = request.POST.get('edit_client_name')
        client_m.phone_number = request.POST.get('edit_phone_number')
        client_m.email_id = request.POST.get('edit_email_id')
        client_m.client_location = request.POST.get('edit_client_location')
        client_m.pan = request.POST.get('edit_pan')
        client_m.contact_person_name = request.POST.get('edit_c_person')        
        client_m.fssai_number = request.POST.get('edit_fssai_number') 
        client_m.client_S_name = request.POST.get('edit_client_S_name') 
        
        client_m.billing_address = request.POST.get('edit_billing_address')
        client_m.billing_city = request.POST.get('edit_billing_city') 
        client_m.billing_state = request.POST.get('edit_billing_state')         
        client_m.billing_pin = request.POST.get('edit_billing_pin') 
        client_m.billing_gst_number = request.POST.get('edit_billing_gst_number')

        client_m.shipping_address = request.POST.get('edit_shipping_address')
        client_m.shipping_city = request.POST.get('edit_shipping_city')         
        client_m.shipping_state = request.POST.get('edit_shipping_state') 
        client_m.shipping_pin = request.POST.get('edit_shipping_pin')
        client_m.shipping_gst_number = request.POST.get('edit_shipping_gst_number')

        client_m.upadated_date = timezone.now() + timedelta(hours=5, minutes=30)
        client_m.updated_by = data.user_id 

        client_m.save()

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
            error_msg = 'Password mismatch. Please try again.'
            combined_context['error_msg'] = error_msg
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
            created_by=data.user_id
        )
        Client_user_new.save()      

        Client_PWD_new = Client_PWD(
            user_id = new_user_id,
            first_name = first_name,
            password = password
        )       
        Client_PWD_new.save() 

        success_msg = 'Client User added successfully.'
        combined_context['success_msg'] = success_msg
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

        com_user.password = request.POST.get('edit_password')
        confirm_password = request.POST.get('edit_confirm_password')

        if com_user.password != confirm_password:
            error_msg = 'Password mismatch. Please try again.'
            return render(request, 'manil_temp/cust_user_master.html', {'error_msg':error_msg})
        
        com_user.upadated_date = timezone.now() + timedelta(hours=5, minutes=30)
        com_user.updated_by = data.user_id 
        
        com_user.save()

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
        
        print('cgst_rate', cgst_rate)   

        context = {
            'material_name':material_name, 'hsn_code':hsn_code, 'cgst_rate':cgst_rate, 'sgst_rate':sgst_rate,
            'igst_rate':igst_rate, 'start_date':start_date, 'end_date':end_date
        }

        if materials.exists():
            for i in materials:
                if i.hsn_code == hsn_code:
                    error_msg = 'This HNS Code is already in use.'
                    return render(request, 'manil_temp/material_master.html', {'data':data,'materials': materials, 'error_msg':error_msg, **context})

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
            created_by=data.user_id  # Assuming you have user authentication
        )
        new_material.save()

        success_msg = 'Materiral added successfully.'
        return render(request, 'manil_temp/material_master.html', {'data':data,'materials': materials, 'success_msg':success_msg})
    
    return render(request, 'manil_temp/material_master.html', {'data':data,'materials': materials})


def edit_material_master(request, id):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)

    materials = get_object_or_404(Material_Master, id=id)

    if request.method == 'POST':
        materials.material_name = materials.material_name     
        materials.hsn_code = request.POST.get('edit_hsn_code')
        materials.unit_of_measurement = request.POST.get('edit_uom')
        materials.Base_Price = request.POST.get('edit_Base_Price')
        materials.cgst_rate = Decimal(request.POST.get('edit_cgst_rate'))
        materials.sgst_rate = Decimal(request.POST.get('edit_sgst_rate'))
        materials.igst_rate = request.POST.get('edit_igst_rate')
        materials.start_date = request.POST.get('edit_start_date')
        materials.end_date = request.POST.get('edit_end_date')
        materials.upadated_date = timezone.now() + timedelta(hours=5, minutes=30)
        materials.updated_by = data.user_id 
 
        materials.save()
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
        
        cost_per_unit = request.POST.get('cost_per_unit')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        mat_rec = Material_Master.objects.get(material_code = material_code)
               
         
        new_costing = Costing_Table(
            client_id=client_id,  
            client_name = client_name,
            location=client_location,
            material_code=material_code, 
            material_name = material_name,                       
            cost_per_unit=int(cost_per_unit),
            start_date=start_date,
            end_date=end_date,
            creation_date=timezone.now() + timedelta(hours=5, minutes=30),
            created_by=data.user_id,

            unit_of_measurement=mat_rec.unit_of_measurement,
            Base_Price=mat_rec.Base_Price,
            cgst_rate=mat_rec.cgst_rate,
            sgst_rate=mat_rec.sgst_rate,
            igst_rate=mat_rec.igst_rate,
            
        )
        new_costing.save()

        success_msg = 'Material cost for a client added successfully'
        return render(request, 'manil_temp/material_cost.html', {'data': data, 'costings': costings, 'materials': materials, 'client_m':client_m, 'success_msg':success_msg})
    
    # Fetch all costing table data for display in the table
    
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
        costings.location = costings.location
        costings.material_code = costings.material_code 
        costings.material_name = costings.material_name         
        
        costings.cost_per_unit = request.POST.get('edit_cost_per_unit')
        costings.start_date = request.POST.get('edit_start_date')
        costings.end_date = request.POST.get('edit_end_date')

        costings.upadated_date = timezone.now() + timedelta(hours=5, minutes=30)
        costings.updated_by = data.user_id 

        costings.save()

        return redirect('material_cost')
    
    return render(request, 'manil_temp/material_cost.html', {'data': data, 'costings': costings, 'materials': materials, 'client_m':client_m})


def manil_order_(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)

    m_orders = manil_order.objects.all()


    return render (request, 'manil_temp/manil_order.html', {'data':data, 'm_orders':m_orders})



def client_order_(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)
    all_orders = client_order.objects.all()

    all_client = Client_Master.objects.all()
    all_users = Client_user.objects.all()    
    cost_det = Costing_Table.objects.all()
    mat_list = Material_Master.objects.all()

    context = {'data':data, 'all_orders':all_orders, 'mat_list':mat_list,
    'all_client':all_client, 'all_users':all_users, 'cost_det':cost_det    
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
            client_id = client_id,
            order_number = new_value,
            order_date = timezone.now() + timedelta(hours=5, minutes=30),
            po_authority = po_authority,
            po_authority_date = po_authority_date,
            creation_date = timezone.now() + timedelta(hours=5, minutes=30),
            created_by = data.user_id,
            grand_total = round(float(grand_total)),
            ammount_words = amt_in_words, 

            shipping_address = shipping_address,
            shipping_city = shipping_city,
            shipping_state = shipping_state,
            shipping_pin = shipping_pin,
            status = 'Order Placed'
        )
        client_order_new.save()

        success_msg = 'Your order has been Placed.'
        return render (request, 'manil_temp/client_order.html', {'success_msg':success_msg, **context})


    return render (request, 'manil_temp/client_order.html', context)


def c_order_view(request, ord_no):    
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)

    ord_no = ord_no
    order = client_order.objects.get(order_number = ord_no)

    all_orders = manil_order.objects.all()

    client_det = Client_Master.objects.get(client_id = order.client_id)

    ord_det = client_order_details.objects.filter(order_number = ord_no)

    mat_list = Material_Master.objects.all()

    context = {'data':data, 'order':order, 'client_det':client_det, 
               'ord_det':ord_det, 'mat_list':mat_list}
    
    if request.method == 'POST':
        
        no_of_sec = request.POST.get('no_of_sec')

        order_number = request.POST.get('order_number')

        old_order = client_order.objects.get(order_number = order_number)

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

        
        for i in range(1, int(no_of_sec) + 1):            
            material_name = request.POST.get(f'material_name_{i}')
            uom = request.POST.get(f'uom_{i}')
            qty = request.POST.get(f'qty_{i}')
            base_price = request.POST.get(f'base_price_{i}')
            gst_type = request.POST.get(f'gst_type_{i}')
            gst_rate = request.POST.get(f'gst_rate_{i}')
            gst_amt = request.POST.get(f'gst_amt_{i}')
            sub_total = request.POST.get(f'sub_total_{i}')        

            manil_order_new = manil_order_details(
                process_num = new_value,
                material_name = material_name,
                uom = uom,
                qty = qty,
                base_price = base_price,
                gst_type = gst_type,
                gst_rate = gst_rate,
                gst_amt = round(float(gst_amt)),
                sub_total = round(float(sub_total))
            )
            manil_order_new.save()

        manil_order_new = manil_order(
            process_num = new_value,
            client_id = old_order.client_id,            
            order_number = old_order.order_number,
            order_date = old_order.order_date,
            po_authority = old_order.po_authority,
            po_authority_date = old_order.po_authority_date,
            creation_date = timezone.now() + timedelta(hours=5, minutes=30),
            created_by = data.user_id,
            grand_total = round(float(grand_total)),
            ammount_words = amt_in_words, 

            shipping_address = old_order.shipping_address,
            shipping_city = old_order.shipping_city,
            shipping_state = old_order.shipping_state,
            shipping_pin = old_order.shipping_pin,
            status = 'Order Placed'
        )
        manil_order_new.save()

        old_order.status = 'In Progress'
        old_order.authorisation_date = timezone.now() + timedelta(hours=5, minutes=30)
        old_order.authorised_by = data.user_id
        old_order.save()

        success_msg = 'Your order has been Placed.'
        return render (request, 'manil_temp/c_order_view.html', {'success_msg':success_msg, **context})

    return render (request, 'manil_temp/c_order_view.html', context)


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
            error_msg = 'Password mismatch. Please try again.'        
            return render(request, 'manil_temp/chaipoint_user.html', {'error_msg':error_msg, **context, **context_2 })
        
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
            created_by=data.user_id
        )
        cp_user_new.save()              

        cp_user_pwd = chai_point_user_pwd(
            user_id = new_user_id,
            first_name = first_name,
            password = password
        )       
        cp_user_pwd.save() 
        
        success_msg = 'Chai Point User added successfully.'
        return render(request, 'manil_temp/chaipoint_user.html', {'success_msg':success_msg, **context, **context_2 })

    return render (request, 'manil_temp/chaipoint_user.html', context)


def manil_ticket(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)

    tickets = Ticket_tbl.objects.all()

    return render (request, 'manil_temp/manil_ticket.html', {'data':data, 'tickets':tickets})

def ticket_view(request,ticket_num):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id = user_id)

    tickets=Ticket_tbl.objects.get(ticket_num=ticket_num)
    client_dt=Client_Master.objects.get(client_id=tickets.client_id)

    if request.method == 'POST':
        tickets.res_description = request.POST['res_description']
        tickets.resolved_by = data.user_id
        tickets.resolved_dt = timezone.now() + timedelta(hours=5, minutes=30)
        tickets.status = 'Closed'

        tickets.save()
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
            description=description
        )
        new_robot.save()

        success_msg = 'Robot is added successfully.'
        return render(request, 'manil_temp/robo_master.html', {'robots': robots,'data': data, 'success_msg':success_msg})

    return render(request, 'manil_temp/robo_master.html', {'robots': robots,'data': data})

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
            description=description
        )
        new_robot_detail.save()

        success_msg = 'Robot details are added successfully.'
        return render(request, 'manil_temp/robo_details.html', {'client_m': client_m, 'robots': robots, 'robot_details': robot_details,'data': data, 'success_msg':success_msg })

    return render(request, 'manil_temp/robo_details.html', {'client_m': client_m, 'robots': robots, 'robot_details': robot_details,'data': data })

def invoice_preview(request, ord_no):    
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)

    manil_det = Manil_db.objects.all()
    order = client_order.objects.get(order_number=ord_no)
    client_det = Client_Master.objects.get(client_id=order.client_id)
    ord_det = client_order_details.objects.filter(order_number=ord_no)
    mat_list = Material_Master.objects.all()
    dispatch = Despatch_Details.objects.all()
    
    existing_invoice = M_client_invoice.objects.filter(order_number=order.order_number).exists()
    
    if request.method == 'POST' and not existing_invoice:

        invoice = M_client_invoice.objects.all()

        if invoice.exists():            
            last_name = invoice.last().invoice_num                     
            pre = last_name[:-3]  
            suf = int(last_name[-3:])                        
            new_suf = suf + 1
                    
            new_suffix = f"{new_suf:03}"        
            new_value = pre + new_suffix
        else:           
            new_value = 'INV001'

        new_invoice = M_client_invoice(
            order_number=order.order_number,
            client_id=order.client_id,
            invoice_num=new_value,
            invoice_date=timezone.now() + timedelta(hours=5, minutes=30),
            po_authority=order.po_authority,
            total_price=order.grand_total,
            creation_date=timezone.now() + timedelta(hours=5, minutes=30),
            created_by=data.user_id,
        )
        new_invoice.save()
        
        success_msg = "Invoice generated successfully"
        return render(request, 'manil_temp/invoice_preview.html', {'success_msg': success_msg})
    
    context = {
        'data': data,
        'order': order,
        'client_det': client_det,
        'ord_det': ord_det,
        'mat_list': mat_list,
        'dispatch': dispatch,
        'manil_det': manil_det,
        'show_generate_button': not existing_invoice  
    }
    
    return render(request, 'manil_temp/invoice_preview.html', context)


def order_remarks(request):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)

    dispatch = Despatch_Details.objects.filter(
        remarks__isnull=False,
        remarks_title__isnull=False,
        remarked_by__isnull=False,
        remarked_date__isnull=False
    )

    return render(request, 'manil_temp/order_remarks.html', {'data': data, 'dispatch': dispatch})

def order_remarks_view(request, ord_no):
    user_id = request.session.get('user_id')
    data = Manil_User.objects.get(user_id=user_id)

    dispatch = Despatch_Details.objects.get(process_num = ord_no)
       

    return render(request, 'manil_temp/order_remarks_view.html', {'data': data, 'dispatch': dispatch})




