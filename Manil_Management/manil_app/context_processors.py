from Manil_Management.imports import *


def global_context(request):
    # Initialize default values
    m_order_count = 0
    m_unread_count = 0

    # Check if the user is authenticated
    if request:
        # Fetch order placed count
        m_order_count = client_order.objects.filter(status="Order Placed").count()

        cp_order_count = manil_order.objects.filter(status="Order Placed").count()

        # Fetch notifications and unread count
        m_notifications = Manil_Notification.objects.filter(is_read = False)
        m_unread_count = m_notifications.count()

        cp_notifications = Chaipoint_Notification.objects.filter(is_read = False)
        cp_unread_count = cp_notifications.count()

        c_notifications = Client_Notification.objects.filter(is_read = False)
        c_unread_count = c_notifications.count()

        inv_notifications = Inv_Notification.objects.filter(is_read = False)
        inv_unread_count = inv_notifications.count()

        c_inv_notifications = Client_Inv_Notification.objects.filter(is_read = False)
        c_inv_unread_count = c_inv_notifications.count()

        ticket_notifications = Ticket_Notification.objects.filter(is_read = False)
        ticket_unread_count = ticket_notifications.count()

        c_ticket_notifications = Client_Ticket_Notification.objects.filter(is_read = False)
        c_ticket_unread_count = c_ticket_notifications.count()

    return {
        'm_order_count': m_order_count,
        'm_unread_count': m_unread_count,
        'm_notifications': m_notifications,
        'cp_notifications':cp_notifications,
        'cp_unread_count':cp_unread_count,
        'cp_order_count':cp_order_count,
        'c_unread_count':c_unread_count,
        'c_notifications':c_notifications,
        'inv_notifications':inv_notifications,
        'inv_unread_count':inv_unread_count,
        'c_inv_notifications':c_inv_notifications,
        'c_inv_unread_count':c_inv_unread_count,
        'ticket_notifications':ticket_notifications,
        'ticket_unread_count':ticket_unread_count,
        'c_ticket_notifications':c_ticket_notifications,
        'c_ticket_unread_count':c_ticket_unread_count,

    }