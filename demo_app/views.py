from django.http import HttpResponse
from .models import MyModel
import threading

def create_model(request):
    print(f"View running in thread: {threading.current_thread().name}")
    instance = MyModel.objects.create(name="Test")
    print("Model created")
    return HttpResponse("Model created")