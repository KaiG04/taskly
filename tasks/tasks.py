from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now

from .models import Task

@shared_task
def notify_user_task_is_due_within_24_hours():
    print(f"Testing")
    tasks = Task.objects.filter(deadline__lte=now() + timedelta(hours=24), deadline__gt=now())
    for task in tasks:
        print(f"Preparing to send email for task: {task.title}")
        send_mail(
            subject='Task Due Reminder',
            message=f"Hello {task.created_by.username}! Reminder, your task {task.title} is due in 24 hours.",
            from_email='reminder@taskly.com',
            recipient_list=[task.created_by.email]
        )
        print(f"Email sent for task: {task.title}")
