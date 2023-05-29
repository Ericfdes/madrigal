from django.http import HttpResponse
from django.shortcuts import render, redirect

def staff_only(function):
    def wrap(request, *args, **kwargs):

        if request.user.is_staff or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            return render(request, '404.html')

    return wrap
