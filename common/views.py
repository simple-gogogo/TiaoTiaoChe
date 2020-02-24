from django.shortcuts import redirect


def index(request):
    return redirect('/static/html/test.html')
