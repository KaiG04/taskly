from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now

from .models import Task

@shared_task
def notify_user_task_is_due_within_24_hours():
    tasks = Task.objects.filter(deadline__lte=now() + timedelta(hours=24), deadline__gt=now(),
                                reminder_notification=False, completed=False)
    for task in tasks:
        try:
            send_mail(
                subject='Task Due Reminder',
                message=f'Hello {task.created_by.username}! Reminder, your task "{task.title}" is due within 24 hours.',
                from_email='reminder@taskly.com',
                recipient_list=[task.created_by.email]
            )
            task.reminder_notification=True
            task.save()
        except Exception as e:
            print("Failed to send email for task: {task.title}. Error: {e}")

@shared_task
def notify_user_invitation_to_task_board(user, invited_by, task_board):
    try:
        print("Sending Invitation to Task Board")
        send_mail(
            subject=f"Invitation to {task_board.title}",
            message=f"{user.username} you have been added as a guest to '{task_board.title}' by {invited_by.username}"
                    f" you are now able to add, edit and delete tasks.",
            from_email='invitations@taskly.com',
            recipient_list=[user.email]
        )
        print("Invitation to Task Board Successfully sent")
    except Exception as e:
        print(f"Failed to send email for invitation to task. Error: {e}")