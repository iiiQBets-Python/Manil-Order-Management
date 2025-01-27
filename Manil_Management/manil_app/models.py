from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password




class Manil_db(models.Model):
    
    company_name = models.CharField(max_length=255)
    date_of_incorporation = models.DateField()    
    pan = models.CharField(max_length=50, unique=True)
    fssai_number = models.CharField(max_length=50, blank=True, null=True)
    msme_number = models.CharField(max_length=50, blank=True, null=True)

    bank_name = models.CharField(max_length=100, blank=True, null=True)    
    branch = models.CharField(max_length=100, blank=True, null=True)
    ifsc = models.CharField(max_length=50, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    bank_address = models.TextField(blank=True, null=True)

    billing_gst_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    billing_address = models.TextField()
    billing_city = models.CharField(max_length=50, blank=True, null=True)
    billing_state = models.CharField(max_length=50, blank=True, null=True)
    billing_pin = models.BigIntegerField(null=True)
    
    shipping_gst_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=50, blank=True, null=True)
    shipping_state = models.CharField(max_length=50, blank=True, null=True)
    shipping_pin = models.BigIntegerField(null=True)


    def __str__(self):
        return self.company_name
    
class Manil_User(models.Model):
    user_id = models.CharField(max_length=100, unique=True)    
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)  
    email_id = models.EmailField(null=True)
    phone_number = models.CharField(max_length=30, null=True)
    password = models.CharField(max_length=355)
    role = models.CharField(max_length=50)    
    creation_date = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    deletion_date = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=100, blank=True, null=True)
    pwd_date = models.DateTimeField(null=True) 
    reg_status = models.BooleanField(default=0)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=100,blank=True,null=True)

    def save(self, *args, **kwargs):        
        if self.pk:
            original = Manil_User.objects.get(pk=self.pk)            
            if original.password != self.password:
                self.password = make_password(self.password)
        else:            
            self.password = make_password(self.password)

        super(Manil_User, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name

#new  
class Manil_PWD(models.Model):
    user_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=30, null=True)
    password = models.CharField(max_length=355)

    def save(self, *args, **kwargs):        
        if self.pk:
            original = Manil_PWD.objects.get(pk=self.pk)            
            if original.password != self.password:
                self.password = make_password(self.password)
        else:            
            self.password = make_password(self.password)

        super(Manil_PWD, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name

class Client_Master(models.Model):
    client_id = models.CharField(max_length=100, unique=True)
    client_name = models.CharField(max_length=255)    
    client_S_name = models.CharField(max_length=255, null=True)
    client_location = models.CharField(max_length=255)
    pan = models.CharField(max_length=50)
    fssai_number = models.CharField(max_length=50, blank=True, null=True)    
    contact_person_name = models.CharField(max_length=100)
    email_id = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50)

    billing_address = models.TextField()
    billing_gst_number = models.CharField(max_length=50)
    billing_city = models.CharField(max_length=50, null=True)
    billing_state = models.CharField(max_length=50, null=True)
    billing_pin = models.BigIntegerField(null=True)

    shipping_address = models.TextField()    
    shipping_gst_number = models.CharField(max_length=50)
    shipping_city = models.CharField(max_length=50, null=True)
    shipping_state = models.CharField(max_length=50, null=True)
    shipping_pin = models.BigIntegerField(null=True)

    creation_date = models.DateTimeField()
    created_by = models.CharField(max_length=100)    
    deletion_date = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=100, blank=True, null=True)    
    upadated_date = models.DateTimeField( null=True)
    updated_by = models.CharField(max_length=100,null=True)

    
    def __str__(self):
        return self.client_name

#new
class Client_short_name(models.Model):
    client_name = models.CharField(max_length=255)
    client_S_name = models.CharField(max_length=255)
    client_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.client_name

class Costing_Table(models.Model):
    client_id = models.CharField(max_length=100) 
    client_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)    
    material_code = models.CharField(max_length=50)
    material_name = models.CharField(max_length=255)    
    hsn_code = models.CharField(max_length=10)
    cost_per_unit = models.BigIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    creation_date = models.DateTimeField()
    created_by = models.CharField(max_length=100) 
    updated_date = models.DateTimeField( null=True)
    updated_by = models.CharField(max_length=100,null=True)

    unit_of_measurement = models.CharField(max_length=50, null=True)   
    Base_Price = models.BigIntegerField(null=True)
    cgst_rate = models.DecimalField(null=True, max_digits=5, decimal_places=2, default=0.00)
    sgst_rate = models.DecimalField(null=True, max_digits=5, decimal_places=2, default=0.00)
    igst_rate = models.BigIntegerField(null=True)
    conversion_rate = models.IntegerField(default=1)


    def __str__(self):
        return self.client_name

class Material_Master(models.Model):
    material_code = models.CharField(max_length=50)
    hsn_code = models.CharField(max_length=10)
    material_name = models.CharField(max_length=255) 
    unit_of_measurement = models.CharField(max_length=50, null=True)   
    Base_Price = models.BigIntegerField(null=True)
    cgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    sgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    igst_rate = models.BigIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    creation_date = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField( null=True)
    updated_by = models.CharField(max_length=100,null=True)
    conversion_rate = models.IntegerField(default=1)

    def __str__(self):
        return self.material_name
    
class Despatch_Details(models.Model):
    process_num = models.CharField(max_length=100)
    process_date = models.DateTimeField()
    client_id = models.CharField(max_length=100)
    client_name = models.CharField(max_length=255)
    order_number = models.CharField(max_length=100)
    order_date = models.DateTimeField()
    dispatch_date = models.DateTimeField()
    dispatch_lr_num = models.CharField(max_length=100)
    exp_del_dt = models.DateTimeField()
    client_rec_dt = models.DateTimeField(null=True)
    creation_date = models.DateTimeField(null=False)
    created_by = models.CharField(max_length=100, null=False) 
    received_by = models.CharField(max_length=100, null=True)
    received_date = models.DateTimeField(null=True)
   

    def __str__(self):
        return self.process_num
    


class M_client_invoice(models.Model):
    order_number = models.CharField(max_length=100)
    client_id = models.CharField(max_length=100)
    client_name = models.CharField(max_length=255)
    invoice_num = models.CharField(max_length=100)
    invoice_date = models.DateTimeField()
    po_authority = models.CharField(max_length=255 , null=True)
    total_price = models.BigIntegerField(null=True)        
    creation_date = models.DateTimeField()
    created_by = models.CharField(max_length=100)    
    authorisation_date = models.DateTimeField(blank=True, null=True)
    authorised_by = models.CharField(max_length=100, blank=True, null=True)   
    
    def __str__(self):
        return self.invoice_num

class M_client_invoice_det(models.Model):
    invoice_num = models.CharField(max_length=100)
    material_name = models.CharField(max_length=255)
    uom = models.CharField(max_length=50) 
    qty = models.BigIntegerField()

    def __str__(self):
        return self.invoice_num

class Client_user(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)    
    client_id = models.CharField(max_length=100)
    client_name = models.CharField(max_length=255)
    role = models.CharField(max_length=50)     
    email_id = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50)
    password = models.CharField(max_length=355, null=True)
    pwd_date = models.DateTimeField(null=True) 
    reg_status = models.BooleanField(default=0)
    creation_date = models.DateTimeField()
    created_by = models.CharField(max_length=100)    
    deletion_date = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=100, blank=True, null=True) 
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=100,blank=True,null=True)

    def save(self, *args, **kwargs):        
        if self.pk:
            original = Client_user.objects.get(pk=self.pk)            
            if original.password != self.password:
                self.password = make_password(self.password)
        else:            
            self.password = make_password(self.password)
        
        super(Client_user, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name

class Client_PWD(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30, null=True)    
    password = models.CharField(max_length=355)

    def save(self, *args, **kwargs):        
        if self.pk:
            original = Client_PWD.objects.get(pk=self.pk)            
            if original.password != self.password:
                self.password = make_password(self.password)
        else:            
            self.password = make_password(self.password)

        super(Client_PWD, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name
    
#new
class chai_point_user(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)  
    role = models.CharField(max_length=50)     
    email_id = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50)
    password = models.CharField(max_length=355, null=True)
    pwd_date = models.DateTimeField(null=True) 
    reg_status = models.BooleanField(default=0)
    creation_date = models.DateTimeField()
    created_by = models.CharField(max_length=100)    
    updated_date = models.DateTimeField( null=True)
    updated_by = models.CharField(max_length=100,null=True)
    deletion_date = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):        
        if self.pk:
            original = chai_point_user.objects.get(pk=self.pk)            
            if original.password != self.password:
                self.password = make_password(self.password)
        else:            
            self.password = make_password(self.password)
        
        super(chai_point_user, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name

#new
class chai_point_user_pwd(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30, null=True)    
    password = models.CharField(max_length=355)

    def save(self, *args, **kwargs):        
        if self.pk:
            original = chai_point_user_pwd.objects.get(pk=self.pk)            
            if original.password != self.password:
                self.password = make_password(self.password)
        else:            
            self.password = make_password(self.password)

        super(chai_point_user_pwd, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name


class client_order(models.Model):
    client_id = models.CharField(max_length=100)
    client_name = models.CharField(max_length=255)
    order_number = models.CharField(max_length=100)
    order_date = models.DateTimeField()    
    po_authority = models.CharField(max_length=255, null=True)
    po_authority_date = models.DateField(null=True)        
    creation_date = models.DateTimeField()
    created_by = models.CharField(max_length=100)    
    authorisation_date = models.DateTimeField(blank=True, null=True)
    authorised_by = models.CharField(max_length=100, blank=True, null=True)

    grand_total = models.BigIntegerField()
    ammount_words = models.CharField(max_length=200)

    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=50, null=True)
    shipping_state = models.CharField(max_length=50, null=True)
    shipping_pin = models.BigIntegerField(null=True)
    status = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.order_number

class client_order_details(models.Model):
    order_number = models.CharField(max_length=100)
    material_name = models.CharField(max_length=255)
    hsn_code = models.CharField(max_length=10)
    uom = models.CharField(max_length=50) 
    qty = models.BigIntegerField()
    base_price = models.BigIntegerField() 

    gst_type = models.CharField(max_length=50) 
    gst_rate = models.IntegerField()
    gst_amt = models.BigIntegerField(null=True)
    sub_total = models.BigIntegerField()
    total_base = models.BigIntegerField(null=True)

    def __str__(self):
        return self.order_number
    
class manil_order(models.Model):
    process_num = models.CharField(max_length=100)
    client_id = models.CharField(max_length=100)
    client_name = models.CharField(max_length=255)
    order_number = models.CharField(max_length=100)
    order_date = models.DateTimeField()    
    po_authority = models.CharField(max_length=255, null=True)
    po_authority_date = models.DateField(null=True) 
    creation_date = models.DateTimeField()
    created_by = models.CharField(max_length=100)    
    authorisation_date = models.DateTimeField(blank=True, null=True)
    authorised_by = models.CharField(max_length=100, blank=True, null=True)

    grand_total = models.BigIntegerField()
    ammount_words = models.CharField(max_length=200)
    
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=50, null=True)
    shipping_state = models.CharField(max_length=50, null=True)
    shipping_pin = models.BigIntegerField(null=True)
    status = models.CharField(max_length=50, null=True)    

    def __str__(self):
        return self.process_num


class manil_order_details(models.Model):
    process_num = models.CharField(max_length=100)    
    material_name = models.CharField(max_length=255)
    hsn_code = models.CharField(max_length=10)
    uom = models.CharField(max_length=50) 
    qty = models.BigIntegerField()
    base_price = models.BigIntegerField()

    gst_type = models.CharField(max_length=50) 
    gst_rate = models.IntegerField()
    gst_amt = models.BigIntegerField(null=True)
    sub_total = models.BigIntegerField()
    total_base = models.BigIntegerField(null=True)
     

class Robo_Ticket(models.Model):
    client_id = models.CharField(max_length=100)
    client_name = models.CharField(max_length=255)
    robot_id = models.CharField(max_length=50, null=False)
    robot_name = models.CharField(max_length=255)
    ticket_num = models.CharField(max_length=100)
    cmp_description = models.TextField()
    res_description = models.TextField()
    complaint_title = models.CharField(max_length=100)
    ticket_date = models.DateTimeField()
    Maintenance_Date = models.DateTimeField()
    status = models.CharField(max_length=100, null=True)
    creation_date = models.DateTimeField()
    created_by = models.CharField(max_length=100) 
    resolved_dt = models.DateTimeField(null=True)
    resolved_by = models.CharField(max_length=100)   

    def __str__(self):
        return self.ticket_num 
    
class Order_Tickets(models.Model):
    process_num = models.CharField(max_length=100, null=False)
    order_number = models.CharField(max_length=100, null=False)
    client_id = models.CharField(max_length=100)
    client_name = models.CharField(max_length=255)
    ticket_num = models.CharField(max_length=100,null=False)
    ticket_date = models.DateTimeField(null=False)
    remarks_title = models.CharField(max_length=150, null=True)
    remarks = models.TextField(null=True) 
    remarked_by = models.CharField(max_length=100) 
    remarked_date = models.DateTimeField(null=True) 
    resolved_dt = models.DateTimeField(null=True)
    resolved_by = models.CharField(max_length=100)  
    remarks_type = models.CharField(max_length=100)

    def __str__(self):
        return self.ticket_num     
    

class Order_Tickets_details(models.Model):
    order_number = models.CharField(max_length=100, null=False)
    material_name = models.CharField(max_length=255)
    order_qty = models.BigIntegerField()
    received_qty = models.BigIntegerField() 
    uom = models.CharField(max_length=50, null=True, default=None) 

    def __str__(self):
        return self.order_number  
        

class Remarkes_images(models.Model):
    order_number = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Client/report/')

    def __str__(self):
        return self.order_number

class Robot_Master(models.Model):
    robot_id = models.CharField(max_length=50, unique=True)
    robot_name = models.CharField(max_length=255)
    robot_type = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField( null=True)
    updated_by = models.CharField(max_length=100,null=True)

    def _str_(self):
        return self.robot_name

class Robot_Details(models.Model):
    STATUS_CHOICES = [
        ('Operational', 'Operational'),
        ('Maintenance', 'Maintenance'),
        ('Out of Service', 'Out of Service'),
    ]

    client_id = models.CharField(max_length=50, null=False)
    client_name = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=255, null=False)
    robot_id = models.CharField(max_length=50, null=False)
    robot_name = models.CharField(max_length=255)
    robot_type = models.CharField(max_length=100 )
    installation_date = models.DateField()
    l_maintenance_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField( null=True)
    updated_by = models.CharField(max_length=100,null=True)

    def _str_(self):
        return f"{self.client_name} - {self.robot_name}"


class Manil_emails(models.Model):
    username1 = models.CharField(max_length=100)
    email1 = models.EmailField()
    username2 = models.CharField(max_length=100, blank=True, null=True)
    email2 = models.EmailField(blank=True, null=True)
    username3 = models.CharField(max_length=100, blank=True, null=True)
    email3 = models.EmailField(blank=True, null=True)
    username4 = models.CharField(max_length=100, blank=True, null=True)
    email4 = models.EmailField(blank=True, null=True)
    username5 = models.CharField(max_length=100, blank=True, null=True)
    email5 = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.username1


class Chaipoint_emails(models.Model):
    username1 = models.CharField(max_length=100)
    email1 = models.EmailField()
    username2 = models.CharField(max_length=100, blank=True, null=True)
    email2 = models.EmailField(blank=True, null=True)
    username3 = models.CharField(max_length=100, blank=True, null=True)
    email3 = models.EmailField(blank=True, null=True)
    username4 = models.CharField(max_length=100, blank=True, null=True)
    email4 = models.EmailField(blank=True, null=True)
    username5 = models.CharField(max_length=100, blank=True, null=True)
    email5 = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.username1


class Client_emails(models.Model):
    client_id = models.CharField(max_length=50, unique=True)
    username1 = models.CharField(max_length=100)
    email1 = models.EmailField()
    username2 = models.CharField(max_length=100, blank=True, null=True)
    email2 = models.EmailField(blank=True, null=True)
    username3 = models.CharField(max_length=100, blank=True, null=True)
    email3 = models.EmailField(blank=True, null=True)
    username4 = models.CharField(max_length=100, blank=True, null=True)
    email4 = models.EmailField(blank=True, null=True)
    username5 = models.CharField(max_length=100, blank=True, null=True)
    email5 = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.client_id


class Manil_Notification(models.Model):
    order_number = models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)  
    is_read = models.BooleanField(default=False)  

    def __str__(self):
        return self.order_number
    
class Client_Notification(models.Model):
    order_number = models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)  
    is_read = models.BooleanField(default=False)  

    def __str__(self):
        return self.order_number    
    

class Chaipoint_Notification(models.Model):
    order_number = models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)  
    is_read = models.BooleanField(default=False)  

    def __str__(self):
        return self.order_number 
    
class Inv_Notification(models.Model):
    order_number = models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)  
    is_read = models.BooleanField(default=False)  

    def __str__(self):
        return self.order_number     
    
class Client_Inv_Notification(models.Model):
    order_number = models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)  
    is_read = models.BooleanField(default=False)  
    
    def __str__(self):
        return self.order_number       
    
class Ticket_Notification(models.Model):
    ticket_num = models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)  
    is_read = models.BooleanField(default=False)  

    def __str__(self):
        return self.ticket_num     
    
class Client_Ticket_Notification(models.Model):
    ticket_num = models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)  
    is_read = models.BooleanField(default=False)  
    
    def __str__(self):
        return self.ticket_num      
    


class Re_manil_order(models.Model):
    ticket_num = models.CharField(max_length=100,null=True)
    process_num = models.CharField(max_length=100)
    client_id = models.CharField(max_length=100)
    client_name = models.CharField(max_length=255)
    order_number = models.CharField(max_length=100)
    re_order_number = models.CharField(max_length=100, null=True)
    order_date = models.DateTimeField()    
    po_authority = models.CharField(max_length=255, null=True)
    po_authority_date = models.DateField(null=True) 
    creation_date = models.DateTimeField()
    created_by = models.CharField(max_length=100)    
    authorisation_date = models.DateTimeField(blank=True, null=True)
    authorised_by = models.CharField(max_length=100, blank=True, null=True)

    grand_total = models.BigIntegerField()
    ammount_words = models.CharField(max_length=200)
    
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=50, null=True)
    shipping_state = models.CharField(max_length=50, null=True)
    shipping_pin = models.BigIntegerField(null=True)
    status = models.CharField(max_length=50, null=True)    

    def __str__(self):
        return self.process_num

class Re_manil_order_details(models.Model):
    process_num = models.CharField(max_length=100)    
    material_name = models.CharField(max_length=255)
    hsn_code = models.CharField(max_length=10)
    uom = models.CharField(max_length=50) 
    qty = models.BigIntegerField()
    base_price = models.BigIntegerField()

    gst_type = models.CharField(max_length=50) 
    gst_rate = models.IntegerField()
    gst_amt = models.BigIntegerField(null=True)
    sub_total = models.BigIntegerField()
    total_base = models.BigIntegerField(null=True)

class Re_client_order(models.Model):
    client_id = models.CharField(max_length=100)
    client_name = models.CharField(max_length=255)
    order_number = models.CharField(max_length=100)
    order_date = models.DateTimeField()    
    po_authority = models.CharField(max_length=255, null=True)
    po_authority_date = models.DateField(null=True)        
    creation_date = models.DateTimeField()
    created_by = models.CharField(max_length=100)    
    authorisation_date = models.DateTimeField(blank=True, null=True)
    authorised_by = models.CharField(max_length=100, blank=True, null=True)

    grand_total = models.BigIntegerField()
    ammount_words = models.CharField(max_length=200)

    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=50, null=True)
    shipping_state = models.CharField(max_length=50, null=True)
    shipping_pin = models.BigIntegerField(null=True)
    status = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.order_number

class Re_client_order_details(models.Model):
    order_number = models.CharField(max_length=100)
    material_name = models.CharField(max_length=255)
    hsn_code = models.CharField(max_length=10)
    uom = models.CharField(max_length=50) 
    qty = models.BigIntegerField()
    base_price = models.BigIntegerField() 

    gst_type = models.CharField(max_length=50) 
    gst_rate = models.IntegerField()
    gst_amt = models.BigIntegerField(null=True)
    sub_total = models.BigIntegerField()
    total_base = models.BigIntegerField(null=True)

    def __str__(self):
        return self.order_number
    
class Re_Despatch_Details(models.Model):
    process_num = models.CharField(max_length=100)
    process_date = models.DateTimeField()
    client_id = models.CharField(max_length=100)
    client_name = models.CharField(max_length=255)
    order_number = models.CharField(max_length=100)
    order_date = models.DateTimeField()
    dispatch_date = models.DateTimeField()
    dispatch_lr_num = models.CharField(max_length=100)
    exp_del_dt = models.DateTimeField()
    client_rec_dt = models.DateTimeField(null=True)
    creation_date = models.DateTimeField(null=False)
    created_by = models.CharField(max_length=100, null=False) 
    received_by = models.CharField(max_length=100, null=True)
    received_date = models.DateTimeField(null=True)
   

    def __str__(self):
        return self.process_num
    

