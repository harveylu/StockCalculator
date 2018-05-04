# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def result(request):
    # testing = {
    #     "stock": "aapl",
    #     "strategy": "Ethical Investing "
    # }
    return render(request, 'result.html')


def submit(request):
    if request.method == 'POST':
        print request.POST.get('price')
        print request.POST.get('checkbox')
        print request.POST
        checkbox1 = assignbool(request.POST.get('checkbox1'))
        checkbox2 = assignbool(request.POST.get('checkbox2'))
        checkbox3 = assignbool(request.POST.get('checkbox3'))
        checkbox4 = assignbool(request.POST.get('checkbox4'))
        checkbox5 = assignbool(request.POST.get('checkbox5'))
        print type(float(request.POST.get('price')))
        print type(checkbox1)
        print type(checkbox2)
        print type(checkbox3)
        print type(checkbox4)
        print type(checkbox5)
        testing = {
            "stock": request.POST.get('price'),
            "checkbox1": checkbox1,
            "checkbox2": checkbox2,
            "checkbox3": checkbox3,
            "checkbox4": checkbox4,
            "checkbox5": checkbox5
        }
        print request.POST.get('checkbox1')
        print request.POST.get('checkbox2')
        print request.POST.get('checkbox3')
        print request.POST.get('checkbox4')
        print request.POST.get('checkbox5')
        return render(request, 'result.html', {'result': testing})


def assignbool(val):
    if val == "on":
        return True
    else:
        return False
