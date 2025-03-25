# Django Signal Playground

A repository demonstrating Django signal behavior and a custom Python `Rectangle` class.

## Django Signal Demo
A simple Django project to explore:
- Synchronous execution of signals
- Same-thread operation with the caller
- Same-transaction scope with the caller

### Setup
1. Install Django: `pip install django`
2. Run migrations: `python manage.py makemigrations && python manage.py migrate`
3. Start server: `python manage.py runserver`
4. Visit: `http://127.0.0.1:8000/create/`

## Rectangle Class
A Python class meeting these requirements:
- Initialized with `length: int` and `width: int`
- Iterable, yielding `{'length': <value>}` then `{'width': <value>}`

### Run
```bash
python rectangle.py