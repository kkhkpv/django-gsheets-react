from django.http import HttpResponse
from . import tasks


def home(request):
    tasks.task.delay()
    return HttpResponse('<h1>Загружаю данные</h1>')
