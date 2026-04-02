from celery import shared_task

@shared_task
def task_created_notification(user_id, title):
    print(f"[EMAIL] Task '{title}' created successfully for user {user_id}")