from django.shortcuts import render
from django.http import JsonResponse
from onesignal_sdk.client import Client
from push_notifications_app.models import Message
from plyer import notification


def view_messages(request):
    messages = Message.objects.all()
    return render(request, 'view_messages.html', {'messages': messages})


def send_push_notification(message):
    # Initialize OneSignal client with your OneSignal app ID and REST API key
    client = Client(app_id='dc9e5f19-785f-4106-b38b-39c8a62d96c7', rest_api_key='N2U2OTNjMGItNzkzYy00ODMxLWE1NGEtNmU4NTI5ZWVkYTNk')

    # Create a notification payload
    notification_payload = {
        'contents': {'en': message},  # English message content
        'included_segments': ['All']  # Send to all subscribed segments
    }

    # Send the notification
    response = client.send_notification(notification_payload)

    # Check the status code of the response
    if response.status_code == 200:
        # Show desktop notification
        notification.notify(
            title='New Message',
            message=message,
            app_icon=None,  # You can specify an icon path if needed
            timeout=10  # The notification will automatically close after 10 seconds
        )
        return True
    return False


def home(request):
    return render(request, 'home.html')

def receive_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            # Save the message to the database
            Message.objects.create(text=message)  # Uncomment if you have a Message model
            # Send push notification
            send_push_notification(message)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def view_messages(request):
    messages = Message.objects.all()
    return render(request, 'view_messages.html', {'messages': messages})
