from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *



@receiver(post_save, sender=Task)

def task_completed_signal(sender, instance, created, **kwargs):
    if not created and instance.status == "COMPLETED":
        print(f"User completed task: {instance.title}")
        print("Signal triggered")