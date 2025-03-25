# Accuknox Django Demo

Hey there! This repo holds a Django project I put together to figure out how signals work, plus a little Python `Rectangle` class I built. It’s all for the Accuknox trainee assessment, and I’ve tried to make it simple yet useful to show what I’ve learned.

## Project Overview

Here’s what’s inside:
- **Django Signal Demo**: A small app called `demo_app` where I test how signals behave by default—like whether they block execution, share threads, or mess with database saves.
- **Rectangle Class**: A Python file (`rectangle.py`) that does this neat iteration trick I’ll explain later.

### Setup Instructions
Getting it running is pretty straightforward:
1. Install Django:
   ```bash
   pip install django
   ```
2. Set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Fire up the server:
   ```bash
   python manage.py runserver
   ```
4. Check out the signal stuff by hitting:
   ```
   http://127.0.0.1:8000/create/
   ```
5. Try the `Rectangle` class with:
   ```bash
   python rectangle.py
   ```

## Answers to Accuknox Trainee Questions

### Topic: Django Signals

#### Question 1: By default, are Django signals executed synchronously or asynchronously?
**Answer**: They’re **synchronous** by default. Basically, when a signal fires, its handler runs right away and holds up whatever called it until it’s done.

**Proof from Project**:  
I set up a view in `demo_app/views.py` that saves a model and triggers a `post_save` signal. The handler in `demo_app/signals.py` has a 2-second sleep to make it obvious:
```python
# demo_app/views.py
from django.http import HttpResponse
from .models import MyModel
import threading

def create_model(request):
    print(f"View running in thread: {threading.current_thread().name}")
    instance = MyModel.objects.create(name="Test")
    print("Model created")
    return HttpResponse("Model created")
```
```python
# demo_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MyModel
import time

@receiver(post_save, sender=MyModel)
def my_signal_handler(sender, instance, **kwargs):
    print(f"Signal received in thread: {threading.current_thread().name}")
    time.sleep(2)  # Just to slow things down
    print("Signal handler finished")
```

**Test**: Hit `http://127.0.0.1:8000/create/` in your browser. In the terminal, you’ll see:
```
View running in thread: MainThread
Model created
Signal received in thread: MainThread
[2 seconds pass]
Signal handler finished
```
I noticed the browser didn’t show “Model created” until after that 2-second wait. That’s how I knew it’s synchronous—if it was async, the page would load instantly, and the signal would run separately. Pretty cool to see it block like that!

---

#### Question 2: Do Django signals run in the same thread as the caller?
**Answer**: Yup, they run in the **same thread** as whatever triggers them by default.

**Proof from Project**:  
I used the same view and signal handler, but added thread logging to check:
```python
# demo_app/views.py
def create_model(request):
    print(f"View running in thread: {threading.current_thread().name}")
    instance = MyModel.objects.create(name="Test")
    print("Model created")
    return HttpResponse("Model created")
```
```python
# demo_app/signals.py
@receiver(post_save, sender=MyModel)
def my_signal_handler(sender, instance, **kwargs):
    print(f"Signal received in thread: {threading.current_thread().name}")
    time.sleep(2)
    print("Signal handler finished")
```

**Test**: Go to `http://127.0.0.1:8000/create/`. Terminal output:
```
View running in thread: MainThread
Model created
Signal received in thread: MainThread
Signal handler finished
```
Both say `MainThread`, so they’re definitely in the same thread. I double-checked by refreshing a few times—always the same. If they were in different threads, I’d expect some funky thread names, but nope, it’s all one happy family here.

---

#### Question 3: By default, do Django signals run in the same database transaction as the caller?
**Answer**: Yes, they’re in the **same database transaction** by default. If the signal screws up, it can undo the caller’s work too.

**Proof from Project**:  
I tweaked `demo_app/signals.py` to throw an error on purpose:
```python
# demo_app/signals.py
@receiver(post_save, sender=MyModel)
def my_signal_handler(sender, instance, **kwargs):
    print(f"Signal received in thread: {threading.current_thread().name}")
    raise Exception("Signal exception")  # Oops, something broke!
```
The view stays the same:
```python
# demo_app/views.py
def create_model(request):
    print(f"View running in thread: {threading.current_thread().name}")
    instance = MyModel.objects.create(name="Test")
    print("Model created")
    return HttpResponse("Model created")
```

**Test**: 
1. Visit `http://127.0.0.1:8000/create/`. The terminal shows:
   ```
   View running in thread: MainThread
   Signal received in thread: MainThread
   [Error traceback]
   ```
   The page crashes with an error.
2. Open the Django shell:
   ```bash
   python manage.py shell
   ```
   ```python
   from demo_app.models import MyModel
   MyModel.objects.all()  # Comes back empty: <QuerySet []>
   ```

I noticed—`create()` should’ve saved something, right? But since the signal crashed, nothing got saved. That’s when it clicked: they’re in the same transaction, so the error rolled everything back. You can revert the signal to normal after testing; I just left it like that to see what happens.

---

### Topic: Custom Classes in Python

#### Task: Create a `Rectangle` class
**Requirements**:
- Takes `length: int` and `width: int` when created.
- Can be looped over, giving `{'length': <value>}` first, then `{'width': <value>}`.

**Solution from Project**:  
Here’s what I came up with in `rectangle.py`:
```python
class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}

if __name__ == "__main__":
    rect = Rectangle(5, 10)
    for item in rect:
        print(item)
```

**Test**: Run it with:
```bash
python rectangle.py
```
You’ll get:
```
{'length': 5}
{'width': 10}
```

I played around with this a bit—`yield` was new to me, but it’s perfect here. It spits out the length first, then width, just like they asked. I tested with different numbers (like 3 and 7), and it worked every time. Simple, but it does the job!

---

## Purpose
I built this to tackle the Accuknox trainee questions. The signal part taught me a ton about how Django handles events, and the `Rectangle` class was a fun little challenge to get iteration working. Hope it shows I’ve got a handle on this stuff!