# Generated by Django 5.1.4 on 2024-12-30 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='chai_point_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('role', models.CharField(max_length=50)),
                ('email_id', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=355, null=True)),
                ('pwd_date', models.DateTimeField(null=True)),
                ('reg_status', models.BooleanField(default=0)),
                ('creation_date', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('updated_date', models.DateTimeField(null=True)),
                ('updated_by', models.CharField(max_length=100, null=True)),
                ('deletion_date', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='chai_point_user_pwd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('password', models.CharField(max_length=355)),
            ],
        ),
        migrations.CreateModel(
            name='Chaipoint_emails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username1', models.CharField(max_length=100)),
                ('email1', models.EmailField(max_length=254)),
                ('username2', models.CharField(blank=True, max_length=100, null=True)),
                ('email2', models.EmailField(blank=True, max_length=254, null=True)),
                ('username3', models.CharField(blank=True, max_length=100, null=True)),
                ('email3', models.EmailField(blank=True, max_length=254, null=True)),
                ('username4', models.CharField(blank=True, max_length=100, null=True)),
                ('email4', models.EmailField(blank=True, max_length=254, null=True)),
                ('username5', models.CharField(blank=True, max_length=100, null=True)),
                ('email5', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client_emails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=50, unique=True)),
                ('username1', models.CharField(max_length=100)),
                ('email1', models.EmailField(max_length=254)),
                ('username2', models.CharField(blank=True, max_length=100, null=True)),
                ('email2', models.EmailField(blank=True, max_length=254, null=True)),
                ('username3', models.CharField(blank=True, max_length=100, null=True)),
                ('email3', models.EmailField(blank=True, max_length=254, null=True)),
                ('username4', models.CharField(blank=True, max_length=100, null=True)),
                ('email4', models.EmailField(blank=True, max_length=254, null=True)),
                ('username5', models.CharField(blank=True, max_length=100, null=True)),
                ('email5', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client_Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=100, unique=True)),
                ('client_name', models.CharField(max_length=255)),
                ('client_S_name', models.CharField(max_length=255, null=True)),
                ('client_location', models.CharField(max_length=255)),
                ('pan', models.CharField(max_length=50)),
                ('fssai_number', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_person_name', models.CharField(max_length=100)),
                ('email_id', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=50)),
                ('billing_address', models.TextField()),
                ('billing_gst_number', models.CharField(max_length=50)),
                ('billing_city', models.CharField(max_length=50, null=True)),
                ('billing_state', models.CharField(max_length=50, null=True)),
                ('billing_pin', models.BigIntegerField(null=True)),
                ('shipping_address', models.TextField()),
                ('shipping_gst_number', models.CharField(max_length=50)),
                ('shipping_city', models.CharField(max_length=50, null=True)),
                ('shipping_state', models.CharField(max_length=50, null=True)),
                ('shipping_pin', models.BigIntegerField(null=True)),
                ('creation_date', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('deletion_date', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.CharField(blank=True, max_length=100, null=True)),
                ('upadated_date', models.DateTimeField(null=True)),
                ('updated_by', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='client_order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=100)),
                ('client_name', models.CharField(max_length=255)),
                ('order_number', models.CharField(max_length=100)),
                ('order_date', models.DateTimeField()),
                ('po_authority', models.CharField(max_length=255, null=True)),
                ('po_authority_date', models.DateField(null=True)),
                ('creation_date', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('authorisation_date', models.DateTimeField(blank=True, null=True)),
                ('authorised_by', models.CharField(blank=True, max_length=100, null=True)),
                ('grand_total', models.BigIntegerField()),
                ('ammount_words', models.CharField(max_length=200)),
                ('shipping_address', models.TextField()),
                ('shipping_city', models.CharField(max_length=50, null=True)),
                ('shipping_state', models.CharField(max_length=50, null=True)),
                ('shipping_pin', models.BigIntegerField(null=True)),
                ('status', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='client_order_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=100)),
                ('material_name', models.CharField(max_length=255)),
                ('hsn_code', models.CharField(max_length=10)),
                ('uom', models.CharField(max_length=50)),
                ('qty', models.BigIntegerField()),
                ('base_price', models.BigIntegerField()),
                ('gst_type', models.CharField(max_length=50)),
                ('gst_rate', models.IntegerField()),
                ('gst_amt', models.BigIntegerField(null=True)),
                ('sub_total', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Client_PWD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('password', models.CharField(max_length=355)),
            ],
        ),
        migrations.CreateModel(
            name='Client_short_name',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=255)),
                ('client_S_name', models.CharField(max_length=255)),
                ('client_id', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('client_id', models.CharField(max_length=100)),
                ('client_name', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=50)),
                ('email_id', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=355, null=True)),
                ('pwd_date', models.DateTimeField(null=True)),
                ('reg_status', models.BooleanField(default=0)),
                ('creation_date', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('deletion_date', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.CharField(blank=True, max_length=100, null=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Costing_Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=100)),
                ('client_name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('material_code', models.CharField(max_length=50)),
                ('material_name', models.CharField(max_length=255)),
                ('hsn_code', models.CharField(max_length=10)),
                ('cost_per_unit', models.BigIntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('creation_date', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('updated_date', models.DateTimeField(null=True)),
                ('updated_by', models.CharField(max_length=100, null=True)),
                ('unit_of_measurement', models.CharField(max_length=50, null=True)),
                ('Base_Price', models.BigIntegerField(null=True)),
                ('cgst_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, null=True)),
                ('sgst_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, null=True)),
                ('igst_rate', models.BigIntegerField(null=True)),
                ('conversion_rate', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Despatch_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_num', models.CharField(max_length=100)),
                ('process_date', models.DateTimeField()),
                ('client_id', models.CharField(max_length=100)),
                ('client_name', models.CharField(max_length=255)),
                ('order_number', models.CharField(max_length=100)),
                ('order_date', models.DateTimeField()),
                ('dispatch_date', models.DateTimeField()),
                ('dispatch_lr_num', models.CharField(max_length=100)),
                ('exp_del_dt', models.DateTimeField()),
                ('client_rec_dt', models.DateTimeField(null=True)),
                ('creation_date', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('received_by', models.CharField(max_length=100, null=True)),
                ('received_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='M_client_invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=100)),
                ('client_id', models.CharField(max_length=100)),
                ('client_name', models.CharField(max_length=255)),
                ('invoice_num', models.CharField(max_length=100)),
                ('invoice_date', models.DateTimeField()),
                ('po_authority', models.CharField(max_length=255, null=True)),
                ('total_price', models.BigIntegerField(null=True)),
                ('creation_date', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('authorisation_date', models.DateTimeField(blank=True, null=True)),
                ('authorised_by', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='M_client_invoice_det',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_num', models.CharField(max_length=100)),
                ('material_name', models.CharField(max_length=255)),
                ('uom', models.CharField(max_length=50)),
                ('qty', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Manil_db',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('date_of_incorporation', models.DateField()),
                ('pan', models.CharField(max_length=50, unique=True)),
                ('fssai_number', models.CharField(blank=True, max_length=50, null=True)),
                ('msme_number', models.CharField(blank=True, max_length=50, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True)),
                ('branch', models.CharField(blank=True, max_length=100, null=True)),
                ('ifsc', models.CharField(blank=True, max_length=50, null=True)),
                ('account_number', models.CharField(blank=True, max_length=50, null=True)),
                ('bank_address', models.TextField(blank=True, null=True)),
                ('billing_gst_number', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('billing_address', models.TextField()),
                ('billing_city', models.CharField(blank=True, max_length=50, null=True)),
                ('billing_state', models.CharField(blank=True, max_length=50, null=True)),
                ('billing_pin', models.BigIntegerField(null=True)),
                ('shipping_gst_number', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('shipping_address', models.TextField()),
                ('shipping_city', models.CharField(blank=True, max_length=50, null=True)),
                ('shipping_state', models.CharField(blank=True, max_length=50, null=True)),
                ('shipping_pin', models.BigIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Manil_emails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username1', models.CharField(max_length=100)),
                ('email1', models.EmailField(max_length=254)),
                ('username2', models.CharField(blank=True, max_length=100, null=True)),
                ('email2', models.EmailField(blank=True, max_length=254, null=True)),
                ('username3', models.CharField(blank=True, max_length=100, null=True)),
                ('email3', models.EmailField(blank=True, max_length=254, null=True)),
                ('username4', models.CharField(blank=True, max_length=100, null=True)),
                ('email4', models.EmailField(blank=True, max_length=254, null=True)),
                ('username5', models.CharField(blank=True, max_length=100, null=True)),
                ('email5', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='manil_order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_num', models.CharField(max_length=100)),
                ('client_id', models.CharField(max_length=100)),
                ('client_name', models.CharField(max_length=255)),
                ('order_number', models.CharField(max_length=100)),
                ('order_date', models.DateTimeField()),
                ('po_authority', models.CharField(max_length=255, null=True)),
                ('po_authority_date', models.DateField(null=True)),
                ('creation_date', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('authorisation_date', models.DateTimeField(blank=True, null=True)),
                ('authorised_by', models.CharField(blank=True, max_length=100, null=True)),
                ('grand_total', models.BigIntegerField()),
                ('ammount_words', models.CharField(max_length=200)),
                ('shipping_address', models.TextField()),
                ('shipping_city', models.CharField(max_length=50, null=True)),
                ('shipping_state', models.CharField(max_length=50, null=True)),
                ('shipping_pin', models.BigIntegerField(null=True)),
                ('status', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='manil_order_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_num', models.CharField(max_length=100)),
                ('material_name', models.CharField(max_length=255)),
                ('hsn_code', models.CharField(max_length=10)),
                ('uom', models.CharField(max_length=50)),
                ('qty', models.BigIntegerField()),
                ('base_price', models.BigIntegerField()),
                ('gst_type', models.CharField(max_length=50)),
                ('gst_rate', models.IntegerField()),
                ('gst_amt', models.BigIntegerField(null=True)),
                ('sub_total', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Manil_PWD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('password', models.CharField(max_length=355)),
            ],
        ),
        migrations.CreateModel(
            name='Manil_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('email_id', models.EmailField(max_length=254, null=True)),
                ('phone_number', models.CharField(max_length=30, null=True)),
                ('password', models.CharField(max_length=355)),
                ('role', models.CharField(max_length=50)),
                ('creation_date', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('deletion_date', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.CharField(blank=True, max_length=100, null=True)),
                ('pwd_date', models.DateTimeField(null=True)),
                ('reg_status', models.BooleanField(default=0)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Material_Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_code', models.CharField(max_length=50)),
                ('hsn_code', models.CharField(max_length=10)),
                ('material_name', models.CharField(max_length=255)),
                ('unit_of_measurement', models.CharField(max_length=50, null=True)),
                ('Base_Price', models.BigIntegerField(null=True)),
                ('cgst_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('sgst_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('igst_rate', models.BigIntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('creation_date', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('updated_date', models.DateTimeField(null=True)),
                ('updated_by', models.CharField(max_length=100, null=True)),
                ('conversion_rate', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Order_Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_num', models.CharField(max_length=100)),
                ('order_number', models.CharField(max_length=100)),
                ('client_id', models.CharField(max_length=100)),
                ('client_name', models.CharField(max_length=255)),
                ('ticket_num', models.CharField(max_length=100)),
                ('ticket_date', models.DateTimeField()),
                ('remarks_title', models.CharField(max_length=150, null=True)),
                ('remarks', models.TextField(null=True)),
                ('remarked_by', models.CharField(max_length=100)),
                ('remarked_date', models.DateTimeField(null=True)),
                ('resolved_dt', models.DateTimeField(null=True)),
                ('resolved_by', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Remarkes_images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_num', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='Client/report/')),
            ],
        ),
        migrations.CreateModel(
            name='Robo_Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=100)),
                ('client_name', models.CharField(max_length=255)),
                ('robot_id', models.CharField(max_length=50)),
                ('robot_name', models.CharField(max_length=255)),
                ('ticket_num', models.CharField(max_length=100)),
                ('cmp_description', models.TextField()),
                ('res_description', models.TextField()),
                ('complaint_title', models.CharField(max_length=100)),
                ('ticket_date', models.DateTimeField()),
                ('Maintenance_Date', models.DateTimeField()),
                ('status', models.CharField(max_length=100, null=True)),
                ('creation_date', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('resolved_dt', models.DateTimeField(null=True)),
                ('resolved_by', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Robot_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=50)),
                ('client_name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=255)),
                ('robot_id', models.CharField(max_length=50)),
                ('robot_name', models.CharField(max_length=255)),
                ('robot_type', models.CharField(max_length=100)),
                ('installation_date', models.DateField()),
                ('l_maintenance_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Operational', 'Operational'), ('Maintenance', 'Maintenance'), ('Out of Service', 'Out of Service')], max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('creation_date', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('updated_date', models.DateTimeField(null=True)),
                ('updated_by', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Robot_Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('robot_id', models.CharField(max_length=50, unique=True)),
                ('robot_name', models.CharField(max_length=255)),
                ('robot_type', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('creation_date', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('updated_date', models.DateTimeField(null=True)),
                ('updated_by', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
