from django.http import HttpResponse


def hello(request, name):
    return HttpResponse(f'Hello, {name}!')
