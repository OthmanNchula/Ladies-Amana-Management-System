from .models import Notification

def unread_notifications_count(request):
    if request.user.is_authenticated and request.user.is_staff:
        unread_count = Notification.objects.filter(admin=request.user, is_read=False).count()
    else:
        unread_count = 0
    return {'unread_notifications_count': unread_count}
