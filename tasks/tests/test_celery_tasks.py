import pytest
from datetime import timedelta
from unittest.mock import patch

from django.utils.timezone import now

from tasks.models import Task, TaskBoard
from tasks.tasks import notify_user_task_is_due_within_24_hours


@pytest.mark.django_db
@patch('tasks.tasks.send_mail') # Mocking the send_mail function
def test_reminder_email_sent_for_task_due_soon(
        mock_send_mail, create_task):
    """
    Testing if the celery task for reminding users via email only sends email if their task is within 24 hours,
    and both reminder_notification and completed are both set to False.
    Email should  be sent, and mock_send_mail should be called only once, reminder_notification
    should be dynamically updated to True.

    :param mock_send_mail: Comes from the @patch('tasks.tasks.send_mail') decorator and replaces the real send_mail
    function allowing us to test email sending without spamming real emails, also allows us to use assert_called_
    with and once to check if emails are sending the correct amount and details.

    :param celery_worker: Sets up a temporary celery worker for our test to be independently tested
    """
    due_task = create_task()

    # Call the Celery task using .apply() allowing us to test the logic without replying on asynchronous execution
    # Running the task immediately, allowing us to run the task without a broker or worker.
    notify_user_task_is_due_within_24_hours.apply()

    mock_send_mail.assert_called_once() # Ensure only one email is sent to "user"
    args, kwargs = mock_send_mail.call_args
    assert kwargs['recipient_list'] == [due_task.created_by.email]
    due_task.refresh_from_db() # fetches the updated due_task object after completing the task, and refreshes
    # the test database to show correct, newly updated value of reminder_notification.
    assert due_task.reminder_notification is True


@pytest.mark.django_db
@patch('tasks.tasks.send_mail')
def test_no_email_sent_for_task_with_reminder_already_sent(
        mock_send_mail, create_task):
    """
    Testing if the celery task for reminding users via email doesn't send an email if the reminder notification is
    True.
    Email should not be sent, and mock_send_mail should not be called.
    :param mock_send_mail:
    :param celery_worker:
    """
    due_task = create_task(reminder_notification=True)

    notify_user_task_is_due_within_24_hours.apply()

    mock_send_mail.assert_not_called()

    due_task.refresh_from_db()
    assert due_task.reminder_notification is True

@pytest.mark.django_db
@patch('tasks.tasks.send_mail')
def test_no_email_sent_for_completed_tasks(mock_send_mail, user, create_task):
    """
    Test if celery task for reminding users via email doesn't send an email if the task is marked as completed.
    reminder_notification is set to false in order to simulate user completing task within 24 hours of due date
    Email should not be sent, and mock_send_mail should not be called.
    :param mock_send_mail:
    :param celery_worker:
    :param user:
    :param create_task:
    """
    completed_task = create_task(completed=True, reminder_notification=False)

    notify_user_task_is_due_within_24_hours.apply()

    mock_send_mail.assert_not_called()

    completed_task.refresh_from_db()
    assert not completed_task.reminder_notification
    assert completed_task.completed is True

@pytest.mark.django_db
@patch('tasks.tasks.send_mail')
def test_no_email_sent_if_task_due_in_more_than_24_hours(
        mock_send_mail, user, create_task):
    """
    Test if celery task for reminding users via email doesn't send an email if the task due date is greater
    than 24 hours.
    Email should not be sent, and mock_send_mail should not be called.
    :param mock_send_mail:
    :param celery_worker:
    :param user:
    :param create_task:
    """
    not_yet_due_task = create_task(
        completed=False, reminder_notification=False, deadline=now() + timedelta(hours=25))

    notify_user_task_is_due_within_24_hours.apply()

    mock_send_mail.assert_not_called()

    not_yet_due_task.refresh_from_db()
    assert not not_yet_due_task.reminder_notification
    assert not_yet_due_task.completed is False

