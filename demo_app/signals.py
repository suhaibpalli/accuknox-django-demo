from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MyModel
import time
import threading

@receiver(post_save, sender=MyModel)
def my_signal_handler(sender, instance, **kwargs):
    print(f"Signal received in thread: {threading.current_thread().name}")
    time.sleep(5)  # Simulate some work
    print("Signal handler finished")